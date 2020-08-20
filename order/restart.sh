
#!/usr/bin/env bash
export PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
export PYTHONUNBUFFERED=1
eval "$(pyenv init -)"


ps aux | grep python


echo "restarting"
# replace BTCUSDT by your SYMBOL in UPPER CASE, eg. CXCUSDT, and add your symbol parameters in parameter.json
SYMBOL=(EEGUSDT)
length="${#SYMBOL[@]}"
for ((i=0;i<$length;i++));do
    echo "${SYMBOL[$i]}"
    kill `ps aux | grep 'main.py' | grep ${SYMBOL[$i]} | grep -v grep | awk '{print $2}'`
    sleep 1
    nohup python main.py ${SYMBOL[$i]} 2>${SYMBOL[$i]}_err.log > ${SYMBOL[$i]}_out.log &
    sleep 2
done
echo ''


sleep 3
echo "Restarted"
ps aux | grep python
