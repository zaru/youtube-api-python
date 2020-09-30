# YouTube API を Python で叩いてグラフにする

```
python main_task.py channel_list.txt
```

channel_list.txt に取得したいチャンネル ID を1行ずつ記載する。

```
channel_A_id
channel_B_id
channel_C_id
```

特定タスクだけを再実行する事が可能。タスクは `./tasks` ディレクトリにある。

```
python main_task.py channel_list.txt --task channel_statistics_task
```