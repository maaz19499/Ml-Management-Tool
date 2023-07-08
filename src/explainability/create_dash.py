from explainerdashboard import ClassifierExplainer, ExplainerDashboard,RegressionExplainer

import pandas as pd

def dash_explain(model,x,mode):
    
        """
                 It is a Explainer Dashboard tool for model interpretability which interprets the black box models.
    
                Args:
                model:        model used for prediction.
                x    :        Testing data x(input) data.
                y    :        Testing data y(output) data(optional).
                mode :        It is a string value which can be either 'classification' or 'regression'.
                              It is used to determine the type of model.
    
                Returns:
                It returns the Explainer Dashboard object.
    
                Raises:
                ValueError:    If the mode is not 'classification' or 'regression'.
                """
        features = model.feature_names_in_.tolist()
        x = x[features]
        if mode == 'Classification':
            try:
                explainer = ClassifierExplainer(model, x,shap='guess')
            except:
                explainer = ClassifierExplainer(model, x, shap='linear')
            output = ExplainerDashboard(explainer)
        elif mode == 'Regression':
            try:
                explainer = RegressionExplainer(model, x)
            except:
                explainer = RegressionExplainer(model, x, shap='kernel')
            output = ExplainerDashboard(explainer)
        return(output)
