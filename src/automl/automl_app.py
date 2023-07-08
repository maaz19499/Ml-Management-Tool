from src.utils_function.utils import load_yaml
from pandas import DataFrame
from .optimize import RunOpt
from xgboost import XGBClassifier
from sklearn.metrics import accuracy_score, f1_score,recall_score,precision_score
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from lightgbm import LGBMClassifier
#from st_aggrid import AgGrid
import numpy as np

class AutoMLApp:
    def __init__(self,target_col,input_cols,train
                        ,test
                        ,maxiter=10
                        ,class_label=1
                        ,score = 'Accuracy'
                        ,score_to_calc_on='Train') -> None:
        self.xtrain = train[input_cols]
        self.ytrain = train[target_col]
        self.isTestGiven = False
        self.maxiter = maxiter
        self.classlabel = class_label
        self.score = score
        self.score_to_calc_on= score_to_calc_on

        if test is not None:
            self.xtest = test[input_cols]
            self.ytest = test[target_col]
            self.isTestGiven = True
        print("initialized")

    #"C:\Users\Ram.singh2\Desktop\Ascend Learning\Adhoc\mlmgr\src\automl\config\main_params.yaml"
    def get_score_metrics(self,score_metric):
        mapping = {'Accuracy':accuracy_score
                    ,'F1 Score':f1_score
                    ,'Recall':recall_score
                    ,'Precision':precision_score}
        return(mapping.get(score_metric,f1_score))

    def get_model_hyper_params(self,algo_name,config_dir):
        # load main config file that has workflow of all other algorithms
        main_config = load_yaml(config_dir,'main_params.yaml') 

        algo_setting = main_config['algo_supported'].get(algo_name)
        assert algo_setting is not None,f'Selected algorithm {algo_name} is missing in main_params.yaml file'
        
        # We have two files for each algorithm, 1st is default that we have setup
        # and 2nd is modified by user. Objective of this is that user can modify all the files
        # except default one and they can reset by replace user hyper parameter config file
        # with default if needed.
        algo_config_file = algo_setting.get('user_modified_file')
        
        if algo_config_file is None:
            algo_config_file = algo_setting.get('default_param_file')

        assert algo_config_file is not None,f'Config file for {algo_name} is not mentioned in main_params.yaml'
   
        algo_config = load_yaml(config_dir,algo_config_file)
   
        df = DataFrame(algo_config).T.reset_index(drop=False).rename(columns={'index':'Param'})
        
        # grid_data = show_grid(df)
        return(df,algo_config_file)
    
    def run_optim(self,config,algo_name):
 
        if algo_name=='Random Forest':
            algo = RandomForestClassifier
            weight_type='inalgo' # class weight should be inside algo call
        elif algo_name=='XG Boost':
            algo=XGBClassifier
            weight_type='infit' # class weight should be inside algo fit
        elif algo_name=='Gradient Boosting':
            algo = GradientBoostingClassifier
            weight_type='infit' # class weight should be inside algo fit
        elif algo_name=='LightGBM':
            algo = LGBMClassifier
            weight_type='infit' # class weight should be inside algo fit
        else:
            algo=XGBClassifier
            weight_type='infit' # class weight should be inside algo fit

        score_metric = self.get_score_metrics(self.score)
        # assert any([self.score_to_calc_on in ['Train','Test']]),'Given Score to calculate on should be either Train or Test'
        # score_on = 'Train' if self.score_to_calc_on =='Test' and self.isTestGiven is None else self.score_to_calc_on
        score_on = self.score_to_calc_on
        opt = RunOpt(algo
                        ,search_space_df = config
                        ,xtrain = self.xtrain
                        ,ytrain = self.ytrain
                        ,xtest=self.xtest if self.isTestGiven else None
                        ,ytest=self.ytest if self.isTestGiven else None
                        ,max_iter=self.maxiter
                        ,class_label=self.classlabel
                        ,score_metrics=score_metric
                        ,score_to_calc_on=score_on
                        ,weight_type=weight_type
                        ,verbose=False)
        model,best_params = opt.run_exp()
        return(model,best_params)

    def main(self,algo_name,params_grid):
        # assert len(np.unique(self.ytrain)),'Currently this tool is only supporting binnary classificaiton'
        # params_grid,algo_config_file = self.get_model_hyper_params(algo_name=algo_name,config_dir=config_dir)
        algo,best_params=self.run_optim(config =params_grid,algo_name=algo_name)
        return(algo,best_params)



