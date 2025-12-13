import pandas as pd

df_bounding_boxes = pd.read_csv("illinois_places_bounding_boxes.csv")
df_bounding_boxes_shuffled = df_bounding_boxes.sample(frac=1).reset_index(drop=True)
df_bounding_boxes_shuffled.to_csv("illinois_places_bounding_boxes_shuffled.csv", index=False)