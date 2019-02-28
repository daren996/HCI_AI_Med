readme

znzd.txt: raw data crawled from Left-Hand Doctor

dial.txt: processed data
|
|-- id
|-- dial
     |-- obj
          |-- time
          |-- speaker
          |-- content
     |-- obj
     |......
     |-- obj
          |-- time
          |-- speaker
          |-- content (results i.e. diagnoses)
-----------------------------------------------

rst.txt: all results 

All Dialogues: 1312
Number of Uncompleted Dialogues: 389
Number of Dialogues with Results: 923
Number of Dialogues with Results but no Diagnose: 21
Number of Dialogues with Results and Diagnoses: 902


* 带 conventional 表示用对话格式储存
dial_conventional.txt : 所有对话 1312 个
dial_no_rst_conventional.txt : 无结果的对话 389 个
dial_rst_conventional.txt : 有结果的对话 923 个
dial_no_dgn_conventional.txt : 有结果但无诊断的对话 21 个
dial_dgn_conventional.txt : 有诊断的对话 902 个
dial_dgn_200_conventional.txt : 从有诊断的对话中随机挑选了200个



