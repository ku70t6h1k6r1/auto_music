import numpy as np
import tensorflow as tf
import common_function as func
import random
import math

class NNW:
    def __init__(self, i_dim, h_dim, o_dim):
        """
        INPUT_LAYER_CONSTRUCTION
        C
        Db
        ...
        B

        OUTPUT_LAYER_CONSTRUCTION
        C * chord_type
        Db * chord_type
        ...
        B * chord_type
        """
        #各層の次元
        self.i_dim = i_dim
        self.h_dim = h_dim
        self.o_dim = o_dim

        #パラメータ
        self.acc = []
        self.sess = None
        self.train_sep = None

    def construct(self):
        #プレースホルダー作成
        self.X = tf.placeholder(tf.float32, shape=[None,self.i_dim])
        self.T = tf.placeholder(tf.float32, shape=[None,self.o_dim])
        #self.Y = tf.nn.relu(self.T)
        self.Y = self.T

        #Variableを作成
        ## INPUT HIDDEN
        self.w_1 = tf.Variable(tf.truncated_normal([self.i_dim, self.h_dim]))
        self.b_1 = tf.Variable(tf.zeros([self.h_dim]))
        self.z = tf.nn.relu(tf.matmul(self.X, self.w_1) + self.b_1)

        ## HIDDEN OUTPUT
        self.w_2 = tf.Variable(tf.truncated_normal([self.h_dim, self.o_dim]))
        self.b_2 = tf.Variable(tf.zeros([self.o_dim]))
        self.output = tf.nn.softmax(tf.matmul(self.z, self.w_2) + self.b_2)

        #誤差関数は交差エントロピーを使用
        self.cross_entropy = -tf.reduce_sum(self.Y * tf.log(tf.clip_by_value(self.output, 1e-20, 1.0)) + (1 - self.Y) * tf.log(tf.clip_by_value(1 - self.output, 1e-20, 1.0 )))

        #勾配降下法(gradient descent)を使用して最適化(optimization)
        #学習率0.1で交差エントロピーの最小化を行う
        #self.train_step = tf.train.GradientDescentOptimizer(0.1).minimize(self.cross_entropy)
        self.train_step = tf.train.AdamOptimizer(1e-3).minimize(self.cross_entropy)

        #sessionの定義
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def learn(self, input, output):
        #学習を行う
        self.sess.run(self.train_step, feed_dict={self.X:input, self.T:output})
        print(str(self.cross_entropy.eval(session=self.sess, feed_dict={self.X:input, self.T:output})))


class Dataset:
    def __init__(self):
        """
        0:I
        1:Im
        2:I2
        3:I4
        4:Iaug
        5:Idim
        """
        self.chords_dic1 = {\
        0:[0, 4, 7], \
        1:[0, 3, 7], \
        2:[0, 2, 7], \
        3:[0, 5, 7], \
        4:[0, 4, 8], \
        5:[0, 3, 6] \
        }

        self.rootSymbol = ["C","Db","D","Eb","E","F","Gb","G","Ab","A","Bb","B"]
        self.chordSymbol = [" ","m","sus2","sus4","aug","dim"]
        self.tones = {}
        self.setTones(self.chords_dic1)

    def setTones(self, chords_dic):
        for i in range(12 * len(chords_dic)):
            self.tones[i] = np.array(chords_dic[i % len(chords_dic)]) + int(i / len(chords_dic))
            for j in range(len(self.tones[i])):
                self.tones[i][j] = self.clip1oct(self.tones[i][j])

    def convertIndexToSymbol(self, idx, rootSymbol, chordSymbol):
        root = rootSymbol[math.floor(idx / len(chordSymbol))]
        symbol = chordSymbol[idx % len(chordSymbol)]
        return root+symbol

    def createTrainSet(self, chords_dic, exec_n = 10):
        onNote = np.zeros(12)
        onChord = np.zeros(len(chords_dic) * 12)
        rootNote = np.random.randint(0,12)
        print("##############")
        print("root is ", rootNote)
        chordType = np.random.randint(0,len(chords_dic))

        for i in range(exec_n):
            note = chords_dic[chordType][np.random.randint(0,len(chords_dic[chordType]))]
            note = self.clip1oct(note + rootNote)
            onNote[note] = onNote[note] + 1

        onChord[rootNote * len(chords_dic) + chordType] = 1
        #print ("True chord is ", rootNote+chordType)
        return func.simpleStd(onNote) , onChord #INPUT_DATA, OUTPUT_DATA

    def clip1oct(self, note):
        if note > 11:
            return note - 12
        else:
            return note

    def translateMelody(self, melody, t = 0.5):
        output = []
        oneNote = np.zeros(12)
        for i in range(len(melody)):
            if melody[i] > -1:
                oneNote[melody[i]%12] = oneNote[melody[i]%12]  + 1
        return func.softmax(oneNote,t = t)

class createHarmoniseNNW:
    def __init__(self):
        self.chordObj = Dataset()
        self.trainChords = self.chordObj.chords_dic1
        self.nnw = NNW(12, 48, 12 * len(self.trainChords))
        self.nnw.construct()
        self.ckpt_dir = "./tf_model/"

    def learn(self, train_n):
        for i in range(train_n):
            print(i)
            trainData = self.chordObj.createTrainSet(self.trainChords)
            input = trainData[0]
            input = input.reshape(1, len(input))
            output = trainData[1]
            output = output.reshape(1, len(output))
            self.nnw.learn(input, output)

        saver = tf.train.Saver()
        saver.save(self.nnw.sess, self.ckpt_dir)

    def restore(self, input):
        saver = tf.train.Saver()
        saver.restore(self.nnw.sess, self.ckpt_dir)
        input = input.reshape(1, len(input))
        output = self.nnw.sess.run(self.nnw.output, feed_dict={self.nnw.X: input})
        return func.dice(func.softmax(np.array(output[0,]), t = 0.1 ))

#実行用コード
def Create(melody, noteParChord_n = 16): #8か12か16でしょう。
    harmonizeNW = createHarmoniseNNW()
    chordObj = Dataset()
    chords = np.full(len(melody), -1)

    for i in range(int(len(melody)/noteParChord_n)):
        noteFreq = chordObj.translateMelody(melody[i*noteParChord_n : (i+1)*noteParChord_n])
        predictChord = harmonizeNW.restore(input = noteFreq)
        chords[i*noteParChord_n : (i+1)*noteParChord_n] = predictChord

    return chords

#以下、学習と確認用
#execObj = createHarmoniseNNW()
##execObj.learn(100000)
#chordObj = Dataset()

#for i in range(100):
#    trainData = chordObj.createTrainSet(chordObj.chords_dic1)
#    predictChord = execObj.restore(input = trainData[0])
#    trueChord = func.dice(func.softmax(trainData[1], t = 0.1))
#    print("chord is ",chordObj.convertIndexToSymbol(trueChord, chordObj.rootSymbol, chordObj.chordSymbol) )
#    print("predict is ",chordObj.convertIndexToSymbol(predictChord, chordObj.rootSymbol, chordObj.chordSymbol) )

#以下、そのほか
#chordObj = Dataset()
#print(chordObj.tones)
