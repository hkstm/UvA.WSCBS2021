build: build-preprocessing build-train build-predict

build-preprocessing:
	brane unpublish preprocessing 1.0.0 && brane remove preprocessing && brane build -c preprocessing container.yml && brane push preprocessing 1.0.0
build-train:
	brane unpublish train 1.0.0 && brane remove train && brane build -c train container.yml && brane push train 1.0.0
build-predict:
	brane unpublish predict 1.0.0 && brane remove predict && brane build -c predict container.yml && brane push predict 1.0.0