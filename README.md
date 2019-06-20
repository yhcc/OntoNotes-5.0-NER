# OntoNotes-5.0-NER

本repo主要用于将OntoNotes-5.0的数据转换为conll格式，OntoNotes-5.0在*[Towards Robust Linguistic Analysis using OntoNotes](http://www.aclweb.org/anthology/W13-3516)* (Yuchen Zhang, Zhi Zhong, CoNLL 2013)中有一个推荐的train-dev-test分割方案，并且他们提供了将OntoNotes-5.0的数据转换为Conll格式的脚本(http://cemantix.org/data/ontonotes.html) ，与此同时，该网页还提供了一个corrected version V12(目前仅有english的切分)的train-dev-test切分方法。

#### Step 0: clone代码到本地

#### Step 1: 下载官方的OntoNote 5.0的数据

可以从这里下载 [https://catalog.ldc.upenn.edu/LDC2013T19](https://catalog.ldc.upenn.edu/LDC2013T19) ，这份指南可能可以帮助你下载 https://www.zhihu.com/question/67166283/answer/629915159 。然后将结果解压到代码所在的文件夹。
解码之后你的文件夹应该有如下结构（onotenotes-release-5.0是解压后得到的）

```
OntoNotes-5.0-NER
  -conll-formatted-ontenotes-5.0/
  -collect_conll.py
  -README.md
  -..
  -onotenotes-release-5.0/
```


#### Step 2: Running the script to recover words

接下来需要使用python2将*_skel文件和数据结合起来生成conll格式的数据，如果你没有python2的环境，可以用如下的方式创建:
```
$ conda create --name py27 python=2.7
$ source activate py27
```

如果你想对生成v4版本的数据，使用以下的命令(将为所有语言生成对应的conll文件)
```
./conll-formatted-ontonotes-5.0/scripts/skeleton2conll.sh -D ./ontonotes-release-5.0/data/files/data ./conll-formatted-ontonotes-5.0/v4/
```
如果需要生成v12版本的切分，使用以下的命令
```
./conll-formatted-ontonotes-5.0/scripts/skeleton2conll.sh -D ./ontonotes-release-5.0/data/files/data ./conll-formatted-ontonotes-5.0/v12/
```
运行以上的命令之后，会在文件夹(onotenotes-release-5.0中最内层的文件夹)中生成*.gold_conll文件。

#### Step 3: 然后将数据collect起来放入train.txt, dev.txt, test.txt.
由于/pt/中是圣经旧约与新约的内容，里面不包含NER的信息，所以不会包含它们

(0) 通过python collect_conll.py将所有结果聚合起来, 支持选择version， language与domain
```
python collect_conll.py
usage: collect_conll.py [-h] [-v VERSION] [-l LANGUAGE]
                      [-d [DOMAIN [DOMAIN ...]]]

optional arguments:
  -h, --help            show this help message and exit
  -v VERSION, --version VERSION
                        Which version of split, v4 or v12.
  -l LANGUAGE, --language LANGUAGE
                        Which language to collect.
  -d [DOMAIN [DOMAIN ...]], --domain [DOMAIN [DOMAIN ...]]
                        What domains to use. If not specified, all will be
                        used. You can choose from bc bn mz nw tc wb.

```
将在本目录生成对应的目录

(1) 指明需要collect的版本
```
python collect_conll.py -v v4
```
输出为
```
For file:v4/english/train.txt, there are 59924 sentences, 1088503 tokens.
For file:v4/english/dev.txt, there are 8528 sentences, 147724 tokens.
For file:v4/english/test.txt, there are 8262 sentences, 152728 tokens.
```
会生成一个v4目录，目录内的结构
```
OntoNotes-5.0-NER/
  -..
  -v4/
    -english/
      -train.txt
      -dev.txt
      -test.txt
```
生成的结果是还不能直接用于ner训练，因为ner列不是BIO等方式tag的，可以借助fastNLP( https://github.com/fastnlp/fastNLP )的
OntoNoteNERDataLoader读取数据。

v12的版本
```
python collect_conll.py -v v12
```
输出为
```
For file:v12/english/train.txt, there are 94292 sentences, 1903816 tokens.
For file:v12/english/dev.txt, there are 13900 sentences, 279495 tokens.
For file:v12/english/test.txt, there are 10348 sentences, 204235 tokens.
```
(2) 指定langaue
默认为english。v12只有english版本的
```
python collect_conll.py -v v4 -l chinese
```
(3) 指定domain
```
python collect_conll.py -v v4 -d bc bn mz nw 
```
生成的目录将是domain名称concat起来，即v4_bc_bn_mz_nw.

(*) 生成的conll文件格式如下(根据需要选取所需要的列)

    1 Document ID : ``str``
        This is a variation on the document filename
    2 Part number : ``int``
        Some files are divided into multiple parts numbered as 000, 001, 002, ... etc.
    3 Word number : ``int``
        This is the word index of the word in that sentence.
    4 Word : ``str``
        This is the token as segmented/tokenized in the Treebank. Initially the ``*_skel`` file
        contain the placeholder [WORD] which gets replaced by the actual token from the
        Treebank which is part of the OntoNotes release.
    5 POS Tag : ``str``
        This is the Penn Treebank style part of speech. When parse information is missing,
        all part of speeches except the one for which there is some sense or proposition
        annotation are marked with a XX tag. The verb is marked with just a VERB tag.
    6 Parse bit: ``str``
        This is the bracketed structure broken before the first open parenthesis in the parse,
        and the word/part-of-speech leaf replaced with a ``*``. When the parse information is
        missing, the first word of a sentence is tagged as ``(TOP*`` and the last word is tagged
        as ``*)`` and all intermediate words are tagged with a ``*``.
    7 Predicate lemma: ``str``
        The predicate lemma is mentioned for the rows for which we have semantic role
        information or word sense information. All other rows are marked with a "-".
    8 Predicate Frameset ID: ``int``
        The PropBank frameset ID of the predicate in Column 7.
    9 Word sense: ``float``
        This is the word sense of the word in Column 3.
    10 Speaker/Author: ``str``
        This is the speaker or author name where available. Mostly in Broadcast Conversation
        and Web Log data. When not available the rows are marked with an "-".
    11 Named Entities: ``str``
        These columns identifies the spans representing various named entities. For documents
        which do not have named entity annotation, each line is represented with an ``*``.
    12+ Predicate Arguments: ``str``
        There is one column each of predicate argument structure information for the predicate
        mentioned in Column 7. If there are no predicates tagged in a sentence this is a
        single column with all rows marked with an ``*``.
    -1 Co-reference: ``str``
        Co-reference chain information encoded in a parenthesis structure. For documents that do
         not have co-reference annotations, each line is represented with a "-".


#### Reference
http://conll.cemantix.org/2012/data.html

https://github.com/yuchenlin/OntoNotes-5.0-NER-BIO

https://github.com/ontonotes/conll-formatted-ontonotes-5.0

https://github.com/allenai/allennlp


