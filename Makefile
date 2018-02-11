init:
	pip install -r requirements.txt

sim:
	python flipdot/sim.py

demo:
	python demo.py udp

.PHONY: init sim demo
