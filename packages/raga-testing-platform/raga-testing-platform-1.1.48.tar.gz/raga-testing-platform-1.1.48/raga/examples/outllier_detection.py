from raga import *
import datetime

run_name = f"rishabh-OD-SR-testing-Rupali-v2-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
test_session = TestSession(project_name='testingProject',run_name=run_name, profile='dev1')

rules = DriftDetectionRules()
rules.add(type="anomaly_detection", dist_metric="Mahalanobis", _class="ALL", threshold=21.3)
edge_case_detection = data_drift_detection(test_session=test_session,
                                           test_name="Drift-detection-test_AI_dash",
                                           dataset_name="Superresolution_rupali-newest-v2",
                                           embed_col_name = "lr_embeddings",
                                           output_type = "outlier_detection",
                                           rules = rules)
test_session.add(edge_case_detection)

test_session.run()