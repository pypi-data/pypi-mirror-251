import os
import logging
import joblib
import numpy as np
import pandas as pd
from all_utils import prepare_dataset, save_plot
import sys
sys.path.append(os.getcwd())


LOG_PATH = '../logs'
os.makedirs(LOG_PATH,exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_PATH,"running_log.log"),
                    level=logging.INFO,
                    format='[%(asctime)s: %(levelname)s: %(module)s]: %(message)s',
                    filemode='a')


class Perceptron:
    try:
        def __init__(self, eta: float=None, epoch: int=None):
            self.weights = np.random.randn(3) * 1e-4 # random tiny weight
            training = (eta is not None) and (epoch is not None)
            if training:
                logging.info(f"Initial Weight is {self.weights}")
            self.eta = eta
            self.epoch = epoch

        def _z_outcome(self, inputs, weights):
            return np.dot(inputs,weights)
        
        def _create_dir_return_path(self,model_dir,fileName):
            os.makedirs(model_dir, exist_ok=True )
            return os.path.join(model_dir, fileName)

        def activation_funtion(self,z):
            return np.where(z > 0, 1, 0)

        def fit(self,X,y):
            try:
                self.X = X
                self.y = y

                # We have to give some bias with weight to Z outcomes to make model more generalize
                X_with_bias = np.c_[self.X, -np.ones((len(self.X),1))]
                logging.info(f"X with bias : \n{X_with_bias}")

                for epoch in range(self.epoch):
                    logging.info("__"*20)
                    logging.info(f"For epoch >>>>> {epoch}:")
                    logging.info("__"*20)
                    z = self._z_outcome(X_with_bias, self.weights)

                    # if z return less than 0 than activation func return 0 otherwise return 1
                    y_pred = self.activation_funtion(z)
                    logging.info(f"Predicted Value after forward pass : {y_pred}")

                    self.error = self.y - y_pred
                    logging.info(f"Error : {self.error}")

                    # Update Weight
                    self.weights = self.weights + self.eta * np.dot(X_with_bias.T,  self.error)
                    logging.info(f"Updated weight after epoch is : {epoch+1}/{self.epoch} >> {self.weights}")
                    logging.info("##"*20)
            except Exception as e:
                logging.exception(e)
                raise e
            
        logging.info('>>>>> Predicting Output... <<<<<')
        def predict(self,X):
            try:
                X_with_bias = np.c_[X, -np.ones((len(X),1))]
                z = self._z_outcome(X_with_bias, self.weights)
                return self.activation_funtion(z)
            except Exception as e:
                logging.exception(e)
                raise e

        def total_loss(self):
            total_loss = np.sum(self.error)
            logging.info(f"Total loss is : {total_loss}")
            return total_loss

        logging.info('>>>>> Saving Model... <<<<<')
        def save(self,  fileName, model_dir = None):
            try:
                if model_dir is not None:
                    model_file_path = self._create_dir_return_path(model_dir,fileName)
                    joblib.dump(self, model_file_path)
                else:
                    model_file_path = self._create_dir_return_path("../model",fileName)
                    joblib.dump(self, model_file_path)
            except Exception as e:
                logging.exception(e)
                raise e
        logging.info('>>>>> Loading Model... <<<<<')
        def load(self,filePath):
            try:
                logging.info('>>>>> Loading Model Sucessfull <<<<<')
                return joblib.load(filePath)
            except Exception as e:
                logging.exception(e)
                raise e
        
    except Exception as e:
        logging.exception(e)
        raise e
    

def main(data,learning_rate,epoch,modelName,modelplotName,filePath):   
    logging.info(">>> Calling Main Function <<<<<")
    df = pd.DataFrame(data)

    X,y = prepare_dataset(df)
    LEARNING_RATE = learning_rate # lies 0 to 1
    EPOCH = epoch

    Model = Perceptron(eta=LEARNING_RATE,epoch=EPOCH)
    Model.fit(X,y)
    logging.info(Model.total_loss())

    Model.save(model_dir=None, fileName=modelName)
    reload_model = Model.load(filePath=filePath)
   
    logging.info(reload_model.predict([[0,1]]))

    save_plot(df,fileName=modelplotName,model=Model)