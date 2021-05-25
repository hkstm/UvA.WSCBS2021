build: build-preprocessing build-train build-predict

build-preprocessing:
	brane unpublish -f preprocessing 1.0.0 && brane remove -f preprocessing && brane build -c preprocessing container.yml && brane push preprocessing 1.0.0
build-train:
	brane unpublish -f train 1.0.0 && brane remove -f train && brane build -c train container.yml && brane push train 1.0.0
build-predict:
	brane unpublish -f predict 1.0.0 && brane remove -f predict && brane build -c predict container.yml && brane push predict 1.0.0