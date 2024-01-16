import random
from raga import *
import pandas as pd
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

def img_url(x):
    file = x.split("/")[-1]
    return StringElement(f"https://ragatesitng-dev-storage.s3.ap-south-1.amazonaws.com/1/selected_coco_images/{file}")

def annotation_v1(row):
    AnnotationsV1 = ImageDetectionObject()
    for detection in row["AnnotationsV1"]:
        AnnotationsV1.add(ObjectDetection(Id=detection['Id'], ClassId=detection['ClassId'], ClassName=detection['ClassName'], Confidence=detection['Confidence'], BBox= detection['BBox'], Format="xywh_normalized"))
    return AnnotationsV1

def model_inferences(row):
    ModelInferences = ImageDetectionObject()
    for detection in row["ModelInferences"]:
        ModelInferences.add(ObjectDetection(Id=detection['Id'], ClassId=detection['ClassId'], ClassName=detection['ClassName'], Confidence=detection['Confidence'], BBox= detection['BBox'], Format="xywh_normalized"))
    return ModelInferences

def imag_vectors_m1(row):
    ImageVectorsM1 = ImageEmbedding()
    for embedding in row["ImageVectorsM1"]:
        ImageVectorsM1.add(Embedding(embedding))
    return ImageVectorsM1

def roi_vectors_m1(row):
    ROIVectorsM1 = ROIEmbedding()
    for embedding in row["ROIVectorsM1"]:
        ROIVectorsM1.add(id=embedding.get("Id"), embedding_values=embedding.get("embedding"))
    return ROIVectorsM1

def generate_random():
    classes = [
        "Yes",
        "No"
    ]
    return random.choice(classes)

def json_parser(json_file):
    df = pd.read_json(json_file)
    data_frame = pd.DataFrame()
    data_frame["ImageId"] = df["ImageId"].apply(lambda x: StringElement(x))
    data_frame["ImageUri"] = df["SourceLink"].apply(lambda x: img_url(x))
    data_frame["SourceLink"] = df["SourceLink"].apply(lambda x: StringElement(x))
    data_frame["TimeOfCapture"] = df.apply(lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1)
    data_frame["Reflection"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["Overlap"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["CameraAngle"] = df.apply(lambda row: StringElement(random.choice(["Yes", "No"])), axis=1)
    data_frame["AnnotationsV1"] = df.apply(annotation_v1, axis=1)
    data_frame["ModelInferences"] = df.apply(model_inferences, axis=1)
    data_frame["ImageVectorsM1"] = df.apply(imag_vectors_m1, axis=1)
    data_frame["ROIVectorsM1"] = df.apply(roi_vectors_m1, axis=1)
    return data_frame.head(5)

pd_data_frame = json_parser("./assets/COCO_engg_final_updated.json")

#### Want to see in csv file uncomment line below ####
# data_frame_extractor(json_parser("./assets/COCO_engg_final_updated.json")).to_csv("./assets/COCO_engg_final_updated_100.csv", index=False)

schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("ImageUri", ImageUriSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("SourceLink", FeatureSchemaElement())
schema.add("Reflection", AttributeSchemaElement())
schema.add("CameraAngle", AttributeSchemaElement())
schema.add("Overlap", AttributeSchemaElement())
schema.add("Status", InferenceSchemaElement(model="GT"))
schema.add("ModelAPred", InferenceSchemaElement(model="ModelB"))
schema.add("ModelAPredConf", InferenceSchemaElement(model="ModelB"))
schema.add("ROIVectorsM1", RoiEmbeddingSchemaElement(model="ROIModel"))
schema.add("ImageVectorsM1", ImageEmbeddingSchemaElement(model="imageModel"))

run_name = f"run-failure-mode-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="LGXJjQFD899MtVSrNHGH", secret_key="TC466Qu9PhpOjTuLu5aGkXyGbM7SSBeAzYH6HpcP", host="http://3.111.106.226:8080")

# test_session = TestSession(project_name="testingProject", run_name= run_name, access_key="GBEAALGlGsq7HrtU8M2c", secret_key="kpFKGZcP7Q0e1ONEH0kZNOIMS19G4P1f6710ddC0", host="http://13.126.220.245:8080")

cred = DatasetCreds(region="ap-south-1")

#create test_ds object of Dataset instance
test_ds = Dataset(test_session=test_session, 
                  name="fma_image_object_detection_ds-10-v2", 
                  type=DATASET_TYPE.IMAGE,
                  data=pd_data_frame, 
                  schema=schema, 
                  creds=cred)

#load schema and pandas data frame
test_ds.load()