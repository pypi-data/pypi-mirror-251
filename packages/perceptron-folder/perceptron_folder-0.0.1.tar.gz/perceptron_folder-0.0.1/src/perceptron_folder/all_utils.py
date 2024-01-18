import os
import logging
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

LOG_PATH = '../logs'
os.makedirs(LOG_PATH,exist_ok=True)
logging.basicConfig(filename=os.path.join(LOG_PATH,"running_log.log"),
                    level=logging.INFO,
                    format='[%(asctime)s: %(levelname)s: %(module)s]: %(message)s',
                    filemode='a')

logging.info('>>>>> Preparing Dataset is Start <<<<<')
def prepare_dataset(df, target_col = 'y'):
    """it returns label and independent features

    Args:
        df (pd.DataFrame): This is a dataframe
        target_col (str, optional): label col name. Defaults to "y".

    Returns:
        tuple: label and x
    """
    try:
        X = df.drop(target_col, axis = 1)
        y = df[target_col]
        return X,y
    except Exception as e:
        logging.exception(e)
        raise e

logging.info('>>>>> Saving Plot... <<<<<')
def save_plot(df, model,fileName=None,plot_dir='../plot'):
    try:

        def _create_base_plot(df):
            try:
                df.plot(kind="scatter", x="X1", y="X2", c="y", s=100, cmap="coolwarm")
                plt.axhline(y=0, color="black", linestyle="--",linewidth=1)
                plt.axvline(x=0, color="black", linestyle="--",linewidth=1)

                figure = plt.gcf()
                figure.set_size_inches(10,8)
            except Exception as e:
                logging.exception(e)
                raise e

        def _plot_decision_region(X,y, model, resolution=0.02):
            try:
                colors = ("cyan", "lightgreen")
                cmap = ListedColormap(colors)

                X = X.values
                x1 = X[:,0]
                x2 = X[:,1]

                x1_min, x1_max = x1.min() - 1, x1.max() + 1
                x2_min, x2_max = x2.min() - 1, x2.max() + 1

                xx1, xx2 = np.meshgrid(np.arange(x1_min,x1_max,resolution),
                                    np.arange(x2_min,x2_max,resolution))
                
                y_pred = model.predict(np.array([xx1.ravel(),xx2.ravel()]).T)
                y_pred = y_pred.reshape(xx1.shape)

                plt.contourf(xx1,xx2,y_pred,alpha=0.2,cmap=cmap)
                plt.xlim(xx1.min(),xx1.max())
                plt.ylim(xx2.min(),xx2.max())

                plt.plot()     
            except Exception as e:
                logging.exception(e)
                raise e

        X,y = prepare_dataset(df)
        logging.info('>>>>> Preparing Dataset is Done <<<<<')

        _create_base_plot(df)
        _plot_decision_region(X,y,model)

        os.makedirs(plot_dir, exist_ok=True)
        plot_path = os.path.join(plot_dir,fileName)

        plt.savefig(plot_path)
    except Exception as e:
        logging.exception(e)
        raise e