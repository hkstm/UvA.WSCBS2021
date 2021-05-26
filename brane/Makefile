build: build-preprocessing build-training build-predicting

build-preprocessing:
	brane unpublish -f preprocessing 1.0.0 && brane remove -f preprocessing && brane build -c preprocessing container.yml && brane push preprocessing 1.0.0
build-training:
	brane unpublish -f training 1.0.0 && brane remove -f training && brane build -c training container.yml && brane push training 1.0.0
build-predicting:
	brane unpublish -f predicting 1.0.0 && brane remove -f predicting && brane build -c predicting container.yml && brane push predicting 1.0.0
build-visualization:
	brane unpublish -f visualization 1.0.0 && brane remove -f visualization && brane build -c visualization container.yml && brane push visualization 1.0.0