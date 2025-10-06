import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import random

load_dotenv()

DISCORD_TOKEN = os.getenv('dicebot_token')

# bot起動時の設定
client = discord.Client(intents=discord.Intents.all())
tree = app_commands.CommandTree(client)

# bot起動時の処理
@client.event
async def on_ready():
    print('ログインしました')
    await tree.sync()

# # メッセージ受信時の処理
# @client.event
# async def on_message(message):
#     # メッセージ送信者がボットの場合は無視する
#     if message.author.bot:
#         return

#     # メッセージの内容をオウム返しする
#     received_message = message.content # 受信したメッセージ
#     print(received_message) # 受信したメッセージを出力
#     if received_message == "ya":
#         await message.channel.send(received_message) # 受信したメッセージを送信
#     return

# client.run(DISCORD_TOKEN)

index_of_d = []
index_of_operator = []
list_of_operator = []
elements_of_roll = []
result_of_roll_show = []
result_of_roll_calc = []

# ダイスを振る関数
def roll_dice(num_of_dice, num_of_faces):
    results = []
    for _ in range(num_of_dice):
        result = random.randint(1, num_of_faces)
        results.append(result)
    return results

# ロールコマンドの実装
@tree.command(name="dice_roll", description="ダイスと気がふれるぜ")
async def dice_roll_command(interaction: discord.Interaction, roll: str):
    # メッセージ送信者がボットの場合は無視する
    if interaction.user.bot:
        return

    print("ロールコマンドが実行されました")
    # メッセージからロールの内容を取得する
    roll_command = roll

    # ロールコマンドの前処理
    roll_command = roll_command.replace(' ', '')
    roll_command = roll_command.replace('　', '')
    roll_command = roll_command.replace('D', 'd')
    roll_command = roll_command.replace('Ｄ', 'd')
    roll_command = roll_command.replace('ｄ', 'd')
    roll_command = roll_command.replace('＊', '*')
    roll_command = roll_command.replace('／', '/')
    roll_command = roll_command.replace('＋', '+')
    roll_command = roll_command.replace('－', '-')
    roll_command = roll_command.replace('−', '-')
    roll_command = roll_command.replace('·', '*')
    roll_command = roll_command.replace('・', '*')
    roll_command = roll_command.replace('﹡', '*')
    roll_command = roll_command.replace('⁎', '*')
    roll_command = roll_command.replace('x', '*')
    roll_command = roll_command.replace('×', '*')
    roll_command = roll_command.replace('÷', '/')
    print(roll_command)
    # ロールの内容を解析
    try:
        for i in range(len(roll_command)):
            if roll_command[i] == 'd':
                index_of_d.append(i)
            elif roll_command[i] == '+' or roll_command[i] == '-' or roll_command[i] == '*' or roll_command[i] == '/':
                index_of_operator.append(i)
                list_of_operator.append(roll_command[i])

        # ロールの内容を要素に分解
        if index_of_operator != []:
            for i in range(len(index_of_operator)):
                if i == 0:
                    elements_of_roll.append(roll_command[0:index_of_operator[i]])
                else:
                    elements_of_roll.append(roll_command[index_of_operator[i-1]+1:index_of_operator[i]])
            elements_of_roll.append(roll_command[index_of_operator[-1]+1:])
        else:
            elements_of_roll.append(roll_command)
        print(elements_of_roll)

        # 各要素を計算
        for element in elements_of_roll:
            if 'd' in element:
                num_of_dice = int(element[0:element.index('d')]) if element[0:element.index('d')] != '' else 1
                num_of_faces = int(element[element.index('d')+1:])
                roll_results = roll_dice(num_of_dice, num_of_faces)
                result_of_roll_show.append(f"{sum(roll_results)}{roll_results}")
                result_of_roll_calc.append(sum(roll_results))
            else:
                result_of_roll_show.append(f"{element}")
                result_of_roll_calc.append(int(element))
        print(result_of_roll_show)
        print(result_of_roll_calc)

        # 計算結果を組み立てる
        calculation_expression = str(result_of_roll_calc[0])
        for i in range(len(list_of_operator)):
            calculation_expression += f" {list_of_operator[i]} {result_of_roll_calc[i+1]}"
        print(calculation_expression)
        final_result = eval(calculation_expression)
        print(final_result)

        show_message = ""
        for i in range(len(result_of_roll_show)):
            if i == 0:
                show_message += result_of_roll_show[i]
            else:
                show_message += f" {list_of_operator[i-1]} {result_of_roll_show[i]}"
        print(show_message)

        # 結果を送信
        await interaction.response.send_message(f"[{show_message}] => {final_result}")

        # 要素のリセット
        index_of_d.clear()
        index_of_operator.clear()
        list_of_operator.clear()
        elements_of_roll.clear()
        result_of_roll_show.clear()
        result_of_roll_calc.clear()
    except Exception as e:
        await interaction.response.send_message("ロールコマンドの形式が正しくありません。")
        print(e)

        # 要素のリセット
        index_of_d.clear()
        index_of_operator.clear()
        list_of_operator.clear()
        elements_of_roll.clear()
        result_of_roll_show.clear()
        result_of_roll_calc.clear()

        
client.run(DISCORD_TOKEN)

