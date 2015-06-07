from sklearn import svm, metrics
import numpy as np



def train( signal , signal_classified ):
	# they should be in the form of:
	# signal, classified signal
	# 1 = stress, 0 = no stress
	n_samples = len( signal ) 
	assert len( signal ) == len( signal_classified ) , 'signal and classified signals are not the same'

	signal = signal.reshape( ( n_samples , 1 ) )
	classifier = svm.SVC()
	# # use the first half of the data to train the classifier
	classifier.fit( signal[:n_samples/2] , signal_classified[:n_samples/2] )
	expected = signal_classified[n_samples/2:]

	predicted = classifier.predict(signal[n_samples/2:])

	print 'confusion matrix:'
	print metrics.confusion_matrix( expected, predicted )
	print 'metrics:'
	print metrics.classification_report(expected, predicted)

	return classifier


if __name__ == '__main__':
	signal, signal_classified = np.random.uniform( 0 , 500 , size = 5000 ), np.random.randint( 0 , 2 , size = 5000 ) # get data from the brain and place it here
	train( signal, signal_classified )


