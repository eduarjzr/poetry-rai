import pandas as pd
from responsibleai.managers.counterfactual_manager import CounterfactualConstants
from raiwidgets import ResponsibleAIDashboard
from responsibleai import RAIInsights
from responsibleai.feature_metadata import FeatureMetadata
import poetry_rai.data.data_paths as data_paths
import poetry_rai.config.settings as settings
from poetry_rai.train.train import get_train_model

from poetry_rai.utils.generator_html import HtmlGenerator
from poetry_rai.utils.generator_pdf import PdfGenerator

def main() -> None:
    # Get datasets
    df_train =  pd.read_csv(data_paths.TITANIC_TRAIN)
    df_val =  pd.read_csv(data_paths.TITANIC_VAL)
    
    # Get trained model
    model = get_train_model(df=df_train)

    # You may also create the FeatureMetadata container, identify any feature of 
    # your choice as the identity_feature, specify a list of strings of categorical 
    # feature names via the categorical_features parameter, and specify dropped 
    # features via the dropped_features parameter.
    feature_metadata = FeatureMetadata(categorical_features=[], dropped_features=[])
    
    # RAIInsights accepts the model, the full dataset, the test dataset, 
    # the target feature string and the task type string as its arguments.
    rai_insights = RAIInsights(
        model=model, 
        train=df_train, 
        test=df_val, 
        target_column=settings.TARGET_FEATURE, 
        task_type='classification', # The task to run, can be `classification`, `regression`, or `forecasting`
        feature_metadata=feature_metadata
    )

    # Add the components of the toolbox that are focused on model assessment.

    # Interpretability
    rai_insights.explainer.add()
    # Error Analysis
    rai_insights.error_analysis.add()
    # Counterfactuals: accepts total number of counterfactuals to generate.
    rai_insights.counterfactual.add(
        total_CFs=20, 
        desired_class=CounterfactualConstants.OPPOSITE,
        features_to_vary=['Sex_female', 'Sex_male'] # the characteristics you want to vary
    )

    # Once all the desired components have been loaded, compute insights on the test set.
    rai_insights.compute()

    # Finally, visualize and explore the model insights. 
    # Use the resulting widget or follow the link to view this in a new tab.
    ResponsibleAIDashboard(rai_insights)

    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

    # Save the dashboard as PDF 
    pdf_generator = PdfGenerator()
    pdf_generator.save_from_url(
        url='http://localhost:5000', 
        output_file_name="ResponsibleAIDashboard.pdf"
    )
    
    # Save the dashboard as HTML 
    html_generator = HtmlGenerator()
    html_generator.save_from_url(
        url='http://localhost:5000', 
        output_file_name="ResponsibleAIDashboard.html"
    )
    