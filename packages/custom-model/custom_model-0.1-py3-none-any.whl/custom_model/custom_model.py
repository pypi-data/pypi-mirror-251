import mlflow


class CustomModel(mlflow.pyfunc.PythonModel):

    # Define the __init__ method to initialize the model parameters
    def __init__(self, model):
        self.model = model

    def __getstate__(self):
        # return a dictionary of the object's state
        return self.__dict__

    def __setstate__(self, state):
        # restore the object's state from the given dictionary
        self.__dict__.update(state)

    # Define the load_context method to load any artifacts or dependencies
    def load_context(self, context):
        pass

    # Define the predict method to make predictions on new data
    def predict(self, context, model_input):
        model_output = self.model.predict(model_input)
        return model_output
