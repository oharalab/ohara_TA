# 三國のprograms/programsフォルダに配置して実行
# exerciseフォルダとその中に入力用ファイルが作成
import os
import sys
import shutil

folder_list = os.listdir()

# とりあえず15回までまわす
for i in range(1,16):
    ex_s = [name for name in folder_list if 'ex%d_' % i in name and 'old' not in name]
    if len(ex_s)!=0:
        os.makedirs('exercise/ex%d/sentences' % i,exist_ok=True)
        for j in ex_s:
            try:
                num = j.replace('ex%d_' % i, '')
                os.makedirs('exercise/ex%d/answers/ex' % i + num,exist_ok=True)
                os.makedirs('exercise/ex%d/inputs/ex' % i + num,exist_ok=True)
                shutil.copyfile('ex%d_%s/correct.c' % (i,num), 'exercise/ex%d/answers/ex' % i + num + '/ex%d_%s.c' % (i,num))

                # count input.txt file number
                ex_tmp = os.listdir('ex%d_%s' % (i,num))
                inputs = [name for name in ex_tmp if 'input' in name]
                if len(inputs)==1:
                    shutil.copyfile('ex%d_%s/input.txt' % (i,num), 'exercise/ex%d/inputs/ex' % i + num + '/trial1.txt')
                else:
                    for input_num in range(len(inputs)):
                        shutil.copyfile('ex%d_%s/' % (i,num) + inputs[input_num], 'exercise/ex%d/inputs/ex' % i + num + '/trial%d' % (input_num+1) +'.txt')
            except:
                # import traceback
                # traceback.print_exc()
                print('ex%d_%s' % (i,num) + ' cause an Error!')
