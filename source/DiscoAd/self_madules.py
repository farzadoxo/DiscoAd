from discord import (Client,Embed,Member)
from source.database.datacenter import DataBase
from colorama import Fore
import datetime
import random



class SignUp:
    def sign_up(user_id:int):
        try:
            DataBase.cursor.execute(f"INSERT INTO table1 VALUES ({user_id} , 500 , 0 , 0)")
            DataBase.connection.commit()
        except:
            pass





class Logging: 
    # Logging system (bot,users,ads etc.)
    

    async def ad_log(client:Client,jump_link):
        ad_log_channel = client.get_channel('CHANNEL ID')
        new_ad_log_embed = Embed(title="تبلیغ جدید ثبت شد ❗",description=jump_link,color=0xffffff)
        try:
            await ad_log_channel.send(embed=new_ad_log_embed)
        except :
            pass


    async def user_log(client:Client,member:Member,amount:int=None,add_coin=False , remove_coin=False , add_warn=False , delete_user=False):

        user_log_channel = client.get_channel('CHANNEL ID')
        user_log_embed = Embed(color=0xffffff)
        
        if add_coin == True:
            user_log_embed.add_field(name=f"به کاربری سکه اضافه شد ❗",value=f"""مقدار : {amount}
                                                                                      به کاربر : {member.mention}""")
            await user_log_channel.send(embed=user_log_embed)

        elif remove_coin == True:
            user_log_embed.add_field(name="از کاربری سکه کم شد ❗",value=f"""مقدار : {amount}
                                                                                    از کاربر : {member.mention}""")
            await user_log_channel.send(embed=user_log_embed)

        elif add_warn == True:
            user_log_embed.add_field(name=" به کاربری اخطار اضافه شد ❗",value=f"به کاربر : {member.mention}")
            await user_log_channel.send(embed=user_log_embed)
        
        elif delete_user == True:
            user_log_embed.add_field(name="کاربری حذف شد ❗",value=f"کاربر : {member.mention}")
            await user_log_channel.send(embed=user_log_embed)


        
    async def bot_log(client:Client,connected=False,ready=False,resumed=False):
        bot_log_channel = client.get_channel('CHANNEL ID')
        api_reconnector_method = ["ssl","ssh","http"]
        
        if connected == True:
            connect_log_embed = Embed(title="Client successfully connected to Discord API 💡",color=0x00ff00)
            connect_log_embed.add_field(name="📡 Ping :",value=f"`{int(client.latency * 1000)}/ms`")
            connect_log_embed.add_field(name="📟 Server Status :",value="OK")
            connect_log_embed.set_footer(text=datetime.datetime.now())
            
            await bot_log_channel.send(embed=connect_log_embed)

        if ready == True:
            print(Fore.GREEN+"Client ready ! :)"+Fore.RESET)
            
        if resumed == True:
            resume_log_embed = Embed(title="Client successfully reconnect to Discord API 🔌",color=0x0000ff)
            resume_log_embed.add_field(name="📡 Ping :",value=int(client.latency * 1000))
            resume_log_embed.add_field(name="🔒 API reconnector method :",value=f"`{random.choise(api_reconnector_method)}`")
            resume_log_embed.set_footer(text=datetime.datetime.now())
            
            await bot_log_channel.send(embed=resume_log_embed)





class TrackingCode:
        tc = f"Da{random.randint(100000000,900000000)}"
        
        def tracking_code_log(self):
            tracking_code_file = open("tracking_codes.txt",'a')
            tracking_code_file.writelines(f"\n{self.tc}")
            tracking_code_file.close()




# class DataExtractor:
#     def __init__(self , userid:int):
#         self.userid = userid

#     DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {.userid}")
#     item = DataBase.cursor.fetchone()
#     try:
#         # User Data
#         user_balance = item[1]
#         user_ads = item[2]
#         user_warn = item[3]
#     except:
#         pass