from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from textSummarizer.entity import ModelEvaluationConfig
from datasets import load_dataset, load_from_disk
from evaluate import load
import torch
import pandas as pd
from tqdm import tqdm

class ModelEvaluation:
    def __init__(self, config: ModelEvaluationConfig):
        self.config = config


    
    def generate_batch_sized_chunks(self, list_of_elements, batch_size):
        # split the dataset into smaller batches that we can process simultaneously
        for i in range(0, len(list_of_elements), batch_size):
            # returns one batch at a time without loading all batches into memory at once
            yield list_of_elements[i : i + batch_size]


    def calculate_metric_on_test_ds(self, dataset, metric, model, tokenizer,
                                    batch_size=16, device="cuda",
                                    column_text="article",
                                    column_summary="highlights"):
        # generating batches of data
        article_batches = list(self.generate_batch_sized_chunks(dataset[column_text], batch_size))
        target_batches = list(self.generate_batch_sized_chunks(dataset[column_summary], batch_size))

        for article_batch, target_batch in tqdm(
                zip(article_batches, target_batches), total=len(article_batches)):

            inputs = tokenizer(article_batch, max_length=1024, truncation=True,
                            padding="max_length", return_tensors="pt")

            # generating summaries
            summaries = model.generate(input_ids=inputs["input_ids"].to(device),
                                    attention_mask=inputs["attention_mask"].to(device),
                                    length_penalty=0.8, num_beams=8, max_length=128)

            # decoding the generated texts
            decoded_summaries = [tokenizer.decode(s, skip_special_tokens=True,
                                                clean_up_tokenization_spaces=True) for s in summaries]

            # Add the predictions and references to the metric
            metric.add_batch(predictions=decoded_summaries, references=target_batch)

        # Compute the score after processing all batches
        score = metric.compute()

        # Check the structure of score
        print(score)  # Inspect the structure of the score here

        # Adjusting the return based on what score contains
        if isinstance(score, dict):
            return {key: score[key] for key in score}  # Return the values directly if they're floats
        else:
            return score  # Return as is if it's not a dict
        

    def evaluate(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained(self.config.tokenizer_path)
        model_pegasus = AutoModelForSeq2SeqLM.from_pretrained(self.config.model_path).to(device)

        # loading data
        dataset_pt = load_from_disk(self.config.data_path)

        rouge_name = ["rouge1", "rouge2", "rougeL", "rougeLsum"]

        rouge_metric = load('rouge')

        score = self.calculate_metric_on_test_ds(
            dataset_pt["test"][0:50], rouge_metric, model_pegasus, tokenizer, batch_size=5,
            column_text="dialogue", column_summary="summary"
        )

        rouge_dict = {rn: score[rn] for rn in rouge_name}

        df = pd.DataFrame(rouge_dict, index=[f'pegasus'])
        df.to_csv(self.config.metric_file_name, index=False)