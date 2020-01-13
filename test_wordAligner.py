from wordAligner import *
import xlrd
import ast

def test_align_named_entites():

	aligner = Aligner("nltk")
	#namedEntityDataSet contains sentence1, sentence2, expected results
	book = xlrd.open_workbook("nameEntityDataSet.xlsx")
	first_sheet = book.sheet_by_index(0) # get first worksheet
	# it contains 50 sentences
	for i in range(1,51):
		se1 = first_sheet.row_values(i)[1]
		se2 = first_sheet.row_values(i)[2]
		expected_result = first_sheet.row_values(i)[3]
		expected_result = ast.literal_eval(expected_result)
		print("exp:", expected_result)
		observed_result = aligner.align_sentences(se1,se2, False)
		print("obs:", observed_result)
		print(observed_result == expected_result)
		#observed_result = aligner.align_sentences(se1,se2)
		#assert observed_result == expected_result

test_align_named_entites()
