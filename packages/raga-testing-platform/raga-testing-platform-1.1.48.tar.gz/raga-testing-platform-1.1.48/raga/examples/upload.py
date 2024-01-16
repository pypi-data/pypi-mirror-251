from raga import *
import pandas as pd
import datetime
import ast


def replace_url(s3_url):
    parts = s3_url.split("/")
    object_key = "/".join(parts[4:])
    http_url = f"https://raga-engineering.s3.us-east-2.amazonaws.com/super_resolution/{object_key}"
    return http_url


def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp


def embedding_reformat(x):
    x = ast.literal_eval(ast.literal_eval(x)["embeddings"])
    Embeddings = ImageEmbedding()
    for embedding in x:
        Embeddings.add(embedding)
    return Embeddings


def csv_parser(csv_file):
    data_frame = pd.read_csv(csv_file)
    data_frame["ImageId"] = data_frame["id"]
    data_frame["lr_url"] = data_frame["lr_url"].apply(lambda x: replace_url(x))
    data_frame["hr_url"] = data_frame["hr_url"].apply(lambda x: replace_url(x))
    data_frame["hr_embeddings"] = data_frame["hr_embeddings"]
    data_frame["lr_embeddings"] = data_frame["lr_embeddings"]
    data_frame["TimeOfCapture"] = data_frame.apply(
        lambda row: TimeStampElement(get_timestamp_x_hours_ago(row.name)), axis=1
    )
    return data_frame


###################################################################################################

pd_data_frame = csv_parser(
    # "/home/ubuntu/1.1Tdisk/DatasetUpload/super_resolution/DIV2k_valid_final_1.csv"
    # # "/home/ubuntu/1.1Tdisk/DatasetUpload/super_resolution/sr_lr_hr_emb.csv"
    # # "/home/ubuntu/1.1Tdisk/DatasetUpload/super_resolution/sr_lr_hr_emb_1.csv"
    "/Users/rupalitripathi/IdeaProjects/testing-platform-python-client/raga/examples/assets/superresoltion_train2.csv"
)


schema = RagaSchema()
schema.add("ImageId", PredictionSchemaElement())
schema.add("TimeOfCapture", TimeOfCaptureSchemaElement())
schema.add("lr_url", ImageUriSchemaElement())
schema.add("hr_url", GeneratedImageUriSchemaElement())
schema.add("hr_embeddings", ImageEmbeddingSchemaElement(ref_col_name="hr_url"))
schema.add("lr_embeddings", ImageEmbeddingSchemaElement(ref_col_name="lr_url"))

# create test_session object of TestSession instance
test_session = TestSession(project_name="testingProject", profile="dev1")

# test_session = TestSession(
#     project_name="testingProject",
#     run_name="rishabh-loadersuperv5",
#     profile='raga'
# )

run_name = f"rishabh_loader_sr_dd-rupali-testing-v2-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

# dev
# test_session = TestSession(
#     project_name="testingProject",
#     run_name=run_name,
#     access_key="52icdx4BmuVUHCBPZ9P6",
#     secret_key="3Q4RSi8NY4c22PmaDi777S7ExeWJGSkdXvgXO7uZ",
#     aws_raga_access_key="AKIAXVVYGGY2D5FZ2PU4",
#     aws_raga_secret_key="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",
#     aws_raga_role_arn="arn:aws:iam::527593518644:role/s3-access-from-ec2",
#     host="https://backend.dev.ragaai.ai",
# )

cred = DatasetCreds(region="us-east-2")


test_ds = Dataset(
    test_session=test_session,
    name="Superresolution_rupali-newest-v2",
    type=DATASET_TYPE.IMAGE,
    data=pd_data_frame,
    schema=schema,
    creds=cred,
)

test_ds.load()