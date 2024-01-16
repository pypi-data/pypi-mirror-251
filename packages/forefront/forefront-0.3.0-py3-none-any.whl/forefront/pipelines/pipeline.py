from typing import List, Dict, Any



class Pipeline():
    # Initialize the Workflow class with inputs, steps, and an empty messages list
    def __init__(self, name):
        self.name = name
        self.id = "123"
        self.length = 1
    
    def add(self, sample = []):
        self.length += 1
        return 'ok'
    
    def get_length(self):
        return self.length
    
    def create_dataset_from_snapshot(self, name: str):
        return '123'

    @staticmethod
    def from_id(id: str):
        wf = Pipeline.__load_pipeline_from_db(id)
        return Pipeline(wf.inputs, wf.steps)

    def __load_pipeline_from_db(id: str):
        return {
            "inputs": [ "prompt"],
            "steps": []
        }
    
