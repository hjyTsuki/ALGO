import os


def get_datasets(dataset_name = "leetcode"):
    if dataset_name == "leetcode":
        data_path = "../leetcode_data/"
        dataset = []
        md_files = [f for f in os.listdir(data_path) if f.endswith('.md')]
        for file in md_files:
            with open(data_path + file, "r") as fp:
                data = fp.read()
                question = data[: data.find("**Example 1:**")]
                example = data[data.find("**Example 1:**"): data.find("**Constraints:**")]
                constraints = data[data.find("**Constraints:**"): data.find("**Function definition**")]
                func = data[data.find("**Function definition**"): ]
                dataset.append(
                    {
                        "full": data,
                        "question": question,
                        "example": example,
                        "constraints": constraints,
                        "func": func
                    }
                )

        return dataset

    return None