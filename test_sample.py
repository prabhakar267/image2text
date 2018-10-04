from main import main
import tempfile
import os


def check_file(original, testing):
	print("Checking: '{}' ... ".format(original), end="")
	with open(original) as f1:
		with open(testing) as f2:
			assert f1.read() == f2.read(), "Output not equal"
	print("Done!")


def test_pages():
	with tempfile.TemporaryDirectory() as temp_dir:
		main("test-data", temp_dir)

		for file in os.listdir(temp_dir):
			check_file("{dir}/{file}".format(dir=temp_dir, file=file),
					   "test-data/{}".format(file))
					
if __name__ == "__main__":					
	test_pages()