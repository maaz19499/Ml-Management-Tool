
from hyperopt import fmin, tpe, hp, STATUS_OK, Trials
import xgboost as xgb
from src.automl.config import constant

class XGB:
    def __init__(self) -> None:
        pass
    
    def get_params(config):
        assert len(config)>0, 'Given Config file in Xgboost Algo does not have any parameter, please check xgbparams.yaml file'

        space={}
        for k,v in config.items():
            param_error = f"For hyperparameter {k}:"
            criteria_check= set(constant.default_params_range) - set(v.keys())

            assert len(criteria_check)>0,param_error + f"Range parameter {' '.join(criteria_check)} is missing."
            
            dist = constant.distribution_map.get(v['distribution'])
                    
            erro_msg  = param_error + ' Distribution name is wrong and it must be from \n '+' '.join(constant.distribution_map.keys())
            assert dist is not None, erro_msg

            if v['distribution'][0]=='q': # if distribution function starts with q then we need the value of interval
                assert v['interval'] is not None, param_error+' value for interval is missing'
                p1 = dist(k, v['min'], v['max'],v['interval'])
            else:
                p1 = dist(k, v['min'], v['max'])
            space[k]={'range':p1,'dtype':v['dtype']}
        return(space)

    def get_model(self,params=None):
        if params is not None:
            model = xgb.XGBClassifier(**params)
        else:
            model = xgb.XGBClassifier()
        return(model)
    
    @staticmethod
    def call(config):
        space = XGB.get_params(config)
        algo = XGB.get_model()
        return(algo,space)
