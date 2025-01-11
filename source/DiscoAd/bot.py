from discord import (app_commands , Intents  , Interaction ,
                      Status , Activity , ActivityType ,
                        ButtonStyle , TextStyle , Member ,
                        Embed , Colour)
from discord.ext.commands import Bot
from discord.ext import commands
from discord.ui import (Button , View , Modal , TextInput)
from components import welcome_embed , help_embed , get_started_embed
from source.database.datacenter import DataBase
from colorama import Fore , init
from source.DiscoAd.self_madules import (SignUp , Logging , TrackingCode)
import datetime



# convert to cmd (windows terminal)
#init(convert=True)


client = Bot(command_prefix="!",
             intents=Intents.all(),
             status=Status.online,
             activity=Activity(type=ActivityType.watching , name="Billboards"))



@client.event
async def on_connect():
    await Logging.bot_log(client=client,connected=True)


@client.event
async def on_ready():
    await Logging.bot_log(client=client,ready=True)
    try:
        synced = await client.tree.sync()
        print(f"{len(synced)} command synced successfully.")
    except Exception as error :
        print(error)








@client.tree.command(name="order",description="سفارش تبلیغات 📮")
async def order(interaction:Interaction):
    ad_channel = client.get_channel('CHANNEL ID')

    DataBase.cursor.execute(f"SELECT userid , balance , count FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    try:
        user_balance = item[1]
        user_ad_count = item[2]
    except:
        pass
    

    claim_button = Button(label="Claim",emoji="📥")
    report_button = Button(label="Report",emoji="🚫",style=ButtonStyle.gray)

    async def claim_button_callback(interaction:Interaction):
        try:
            DataBase.cursor.execute(f"SELECT userid , balance , count FROM table1 WHERE userid = {interaction.user.id}")
            items = DataBase.cursor.fetchone()

            user_balance = items[1]
            
            if items == None:
                SignUp.sign_up(user_id=interaction.user.id)
                await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
            else:
                DataBase.cursor.execute(f"UPDATE table1 SET balance = {user_balance + 10} WHERE userid = {interaction.user.id}")
                DataBase.connection.commit()
                
                await interaction.response.send_message("**10 سکه گرفتی 🤑**",ephemeral=True)
                
        except:
            pass


    async def report_button_callback(interaction:Interaction):
        report_channel = client.get_channel('CHANNEL ID')

        report_embed = Embed(title="New report ❗",color=Colour.red())
        report_embed.add_field(name="Reported By : ",value=f"{interaction.user.mention}",inline=False)
        report_embed.add_field(name="For :" , value=interaction.message.jump_url,inline=False)

        try:
            await report_channel.send(embed=report_embed)
        except:
            pass
        await interaction.response.send_message("**گزارش جهت بررسی برای تیم مادریتور ارسال شد. لطفا از اسپم خودداری کنید ✅**",ephemeral=True)


    
    claim_button.callback = claim_button_callback
    report_button.callback = report_button_callback

    banner_view = View(timeout=None)
    banner_view.add_item(claim_button)
    banner_view.add_item(report_button)

    

    

    class BannerModal(Modal , title="ارسال بنر"):
        banner = TextInput(label="متن یا بنر تبلیغاتی خود را وارد کنید :",required=True,style=TextStyle.paragraph)

        async def on_submit(self, interaction: Interaction):
           
           try:
               my_tc = TrackingCode()
               banner_info_embed = Embed(color=Colour.random())
               banner_info_embed.add_field(name="👤 Owner :",value=f"{interaction.user.mention}")
               banner_info_embed.add_field(name="🕐 At :" , value=f"{datetime.datetime.now()}")
               message = await ad_channel.send(self.banner,view=banner_view,embed=banner_info_embed,delete_after=86400)
               await Logging.ad_log(client=client,jump_link=message.jump_url)
               DataBase.cursor.execute(f"UPDATE table1 SET balance = {user_balance - 500} , count = {user_ad_count + 1} WHERE userid = {interaction.user.id}")
               DataBase.connection.commit()
               await interaction.response.send_message(f"**بنر با موفقیت ارسال شد و مقدار 500 سکه از حساب شما کسر شد ✅**\n کد پیگیری : {my_tc.tc}",ephemeral=True)
               my_tc.tracking_code_log()
           except Exception as error:
               print(error)
               

    accept_button = Button(label="ثبت سفارش",emoji="✔",style=ButtonStyle.blurple)
    order_view = View(timeout=None)
    order_view.add_item(accept_button)

    async def accept_button_callback(interaction:Interaction):
        await interaction.response.send_modal(BannerModal())
    
    accept_button.callback = accept_button_callback

    

    if item == None:
        SignUp.sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        if user_balance < 500:
            await interaction.response.send_message("**به اندازه کافی سکه نداری 💰**",ephemeral=True)
        else:
            order_embed = Embed(title="**لطفا موارد زیر را مطالعه کنید :**",color=Colour.blurple())
            order_embed.add_field(name="1." , value="**ارسال هرگونه بنر حاوی محتوای جنسی ، کودک آزاری و ... ممنوع میشود.**",inline=False)
            order_embed.add_field(name="2." , value="**بنر ارسال شده قابل ویرایش نیست! در ارسال بنر دقت کنید.**",inline=False)
            order_embed.add_field(name="3." , value="**موضوع بنر ارسالی میتواند تبلیغ سرور دیسکورد ، چنل یوتوب ، سایت و ... باشد**",inline=False)
            order_embed.set_footer(text="در صورت تایید موارد بالا از دکمه ثبت سفارش استفاده کنید ✅")
            await interaction.response.send_message(embed=order_embed,view=order_view,ephemeral=True)







@client.tree.command(name="account_info",description="اطلاعات کاربری من 📋")
async def account_info(interaction:Interaction):
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    if item == None:
        SignUp.sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        account_info_embed = Embed(title="**اطلاعات حساب کاربری شما به صورت زیر میباشد :**",color=Colour.blue())
        account_info_embed.set_author(name=interaction.user.name,icon_url=interaction.user.avatar)
        account_info_embed.add_field(name="🆔 UserID :",value=f"`{interaction.user.id}`",inline=False)
        account_info_embed.add_field(name="💰 Coins :" ,value=f"`{item[1]}`",inline=False)
        account_info_embed.add_field(name="🏷 Ads :",value=f"`{item[2]}`",inline=False)
        account_info_embed.add_field(name="🛑 Warnings :",value=f"`{item[3]}`",inline=False)
        await interaction.response.send_message(embed=account_info_embed,ephemeral=True)






@client.tree.command(name="transfer",description="انتقال سکه به کاربر دیگه 💸")
@app_commands.describe(amount="مقدار سکه جهت انتقال را وارد کنید")
@app_commands.describe(user="فرد موردنظر جهت انتقال سکه را وارد کنید")
async def transfer(interaction:Interaction,amount:int,user:Member):
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
    to = DataBase.cursor.fetchone()

    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    transporter = DataBase.cursor.fetchone()

    if transporter == None:
        SignUp.sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        if to == None:
            SignUp.sign_up(user_id=user.id)
            await interaction.response.send_message("**اطلاعات کاربری این کاربر در دیتابیس یافت نشد. عملیات ثبت نام این کاربر با موفقیت انجام شد لطفا دوباره از این کامند استفاده کنید. ✅**")
        else:
            if amount > transporter[1]:
                await interaction.response.send_message("**سکه های شما کمتر از مقدار موردنظر جهت انتقال است ❗**")
            else:
                try:
                    DataBase.cursor.execute(f"UPDATE table1 SET balance = {transporter[1] - amount} WHERE userid = {interaction.user.id}")
                    DataBase.connection.commit()
                    
                    DataBase.cursor.execute(f"UPDATE table1 SET balance = {to[1] + amount} WHERE userid = {user.id}")
                    DataBase.connection.commit()

                    await interaction.response.send_message(f"**مقدار `{amount}` سکه از کاربر {interaction.user.mention} کسر و به کاربر {user.mention} منتقل شد. ✅**")
                except Exception as error :
                    print(error)






@client.remove_command("help")
@client.tree.command(name="help",description="درباره بات و آموزشات ❓")
async def help(interaction:Interaction):

    

    
    try:
        help_embed.set_author(name=interaction.user.display_name , icon_url=interaction.user.avatar.url)
    except AttributeError:
        help_embed.set_author(name=interaction.user.display_name)
    
    help_embed.set_thumbnail(url='https://png.pngtree.com/png-vector/20190826/ourmid/pngtree-marketing-png-image_1697508.jpg')
    
    get_started_button = Button(label="Get Started !",emoji="🔰",style=ButtonStyle.gray)
    


    async def get_started_button_callback(interaction:Interaction):
        await interaction.response.send_message(embed=get_started_embed,ephemeral=True)

    get_started_button.callback = get_started_button_callback




    help_view = View()
    help_view.add_item(get_started_button)
    
    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {interaction.user.id}")
    item = DataBase.cursor.fetchone()

    if item == None:
        SignUp.sign_up(user_id=interaction.user.id)
        await interaction.response.send_message(embed=welcome_embed,ephemeral=True)
    else:
        await interaction.response.send_message(embed=help_embed,view=help_view,ephemeral=True)







@client.tree.command(name='user_manager',description="مدیریت کاربر 🔒")
@app_commands.default_permissions(administrator=True)
@app_commands.describe(user="کاربر موردنظر رو منشن کنید")
async def user_manager(interaction:Interaction,user:Member):
        DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
        show_item = DataBase.cursor.fetchone()
        #User Data
        try:
            user_balance = show_item[1]
            user_ads = show_item[2]
            user_warn = show_item[3]
        except:
            pass
        manager_embed = Embed(title="کاربر موردنظر با موفقیت از دیتابیس فچ شد",color=Colour.blurple())
        manager_embed.add_field(name="**🆔 UserID :**",value=f"`{user.id}`",inline=False)
        manager_embed.add_field(name="**👤 Mention :**",value=f"{user.mention}",inline=False)
        manager_embed.add_field(name="**💰 Coins :**",value=f"`{user_balance}`",inline=False)
        manager_embed.add_field(name="**🏷 Ads :**",value=f"`{user_ads}`",inline=False)
        manager_embed.add_field(name="**🛑 Warnings :**",value=f"`{user_warn}`",inline=False)
        manager_embed.set_footer(text="چه عملی انجام بدم؟ 😊")


        add_coin_button = Button(label="واریز سکه",emoji="➕",style=ButtonStyle.blurple)
        add_warn_button = Button(label="افزودن اخطار",emoji="⚠",style=ButtonStyle.red)
        remove_coin_button = Button(label="برداشت سکه",emoji="➖",style=ButtonStyle.blurple)
        remove_user_button = Button(label="حذف کاربر",emoji="🗑",style=ButtonStyle.red)



        class AddCoinModal(Modal,title="واریز سکه"):
            add_amount = TextInput(label="چند سکه به کاربر واریز شه؟",required=True,style=TextStyle.short)
            
            async def on_submit(self,interaction:Interaction):
                DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                item = DataBase.cursor.fetchone()
                    #User Data
                    #try:
                        #user_balance = item[1]
                        #user_ads = item[2]
                        #user_warn = item[3]
                    #except:
                        #pass
                if interaction.user.id != 1006459247057436703:
                    pass
                else:
                    try:
                        DataBase.cursor.execute(f"UPDATE table1 SET balance = {item[1] + int(self.add_amount.value)} WHERE userid = {user.id}")
                        DataBase.connection.commit()
                        await Logging.user_log(client=client,member=user,add_coin=True,amount=self.add_amount)
                        await interaction.response.send_message(f"**مقدار {self.add_amount} سکه به کاربر واریز شد. ✅**")
                    except Exception as error:
                        await interaction.response.send_message("**در واریز سکه مشکلی پیش اومد ❌** {}".format(error))


        
        class RemoveCoinModal(Modal , title="برداشت سکه"):
            remove_amount = TextInput(label="چند سکه از کاربر برداشت شه؟",style=TextStyle.short)

            async def on_submit(self , interaction:Interaction):
                DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                item = DataBase.cursor.fetchone()
                    #User Data
                    #try:
                        #user_balance = item[1]
                        #user_ads = item[2]
                        #user_warn = item[3]
                    #except:
                        #pass
                if interaction.user.id != 1006459247057436703:
                    pass
                else:
                    try:
                        if item[1]>= int(self.remove_amount.value):
                            DataBase.cursor.execute(f"UPDATE table1 SET balance = {item[1] - int(self.remove_amount.value)} WHERE userid = {user.id}")
                            DataBase.connection.commit()
                            await Logging.user_log(client=client,member=user,remove_coin=True,amount=self.remove_amount) # Send log to log channel
                            await interaction.response.send_message(f"**مقدار {self.remove_amount} سکه از کاربر برداشت شد. ✅**")
                        else:
                            await interaction.response.send_message("**مقدار سکه کاربر از مقدار برداشت کمتر است ❗**")
                    except Exception as error:
                            await interaction.response.send_message("**در برداشت سکه مشکلی پیش اومد ❌** {}".format(error))




        async def add_warn_button_callback(interaction:Interaction):
            if interaction.user.id != 1006459247057436703:
                pass
            else:
                try:
                    DataBase.cursor.execute(f"SELECT * FROM table1 WHERE userid = {user.id}")
                    item = DataBase.cursor.fetchone()
                    if item[3] + 1 == 3:
                        await user.ban(reason="رعایت نکردن قوانین ثبت بنر 🚫")
                        await interaction.response.send_message("**اخطار های این کاربر به 3 تا رسید. کاربر با موفقیت بن شد ❗**")
                        DataBase.cursor.execute(f"DELETE FROM table1 WHERE userid = {user.id}")
                        DataBase.connection.commit()
                    else:
                        DataBase.cursor.execute(f"UPDATE table1 SET warnings = {item[3] + 1} WHERE userid = {user.id}")
                        DataBase.connection.commit()
                        await Logging.user_log(client=client,member=user,add_warn=True)
                        await interaction.response.send_message("**برای کاربر یک اخطار افزوده شد ✅**")
                except Exception as error:
                    await interaction.response.send_message("**در افزودن اخطار مشکلی پیش اومد ❌**")
                    print(error)


        async def add_coin_button_callback(interaction:Interaction):
            await interaction.response.send_modal(AddCoinModal())



        async def remove_coin_button_callback(interaction:Interaction):
            await interaction.response.send_modal(RemoveCoinModal())

        
        async def remove_user_button_callback(interaction:Interaction):
            if interaction.user.id != 1006459247057436703:
                    pass
            else:
                confirm_view = View()
                confirm_embed = Embed(title="**آیا از حذف کاربر اطمینان دارید؟**",description="با انجام این کار تمامی اطلاعات کاربر از دیتابیس حذف میشود",color=Colour.blurple())
                yes_button = Button(label="بله",emoji="✔",style=ButtonStyle.green)
                no_button = Button(label="نه",emoji="✖",style=ButtonStyle.red)


            async def yes_button_callback(interaction:Interaction):
                try:
                    DataBase.cursor.execute(f"DELETE FROM table1 WHERE userid = {user.id}")
                    DataBase.connection.commit()
                    await Logging.user_log (client=client,member=user,delete_user=True)
                    await interaction.response.send_message("**تمامی اطلاعات کاربر با موفقیت از دیتابیس پاک شد ✅**",ephemeral=True)
                except Exception as error:
                    await interaction.response.send_message(f"**در حذف کاربر خطایی رخ داد دوباره تلاش کنید ❌ {error}**",ephemeral=True)
            
            async def no_button_callback(interaction:Interaction):
                await interaction.response.send_message("**عملیات با موفقیت لغو شد✅**",ephemeral=True)


            yes_button.callback = yes_button_callback
            no_button.callback = no_button_callback

            confirm_view.add_item(yes_button)
            confirm_view.add_item(no_button)
            
            await interaction.response.send_message(embed=confirm_embed,view=confirm_view,ephemeral=True)

            

        add_coin_button.callback = add_coin_button_callback
        add_warn_button.callback = add_warn_button_callback
        remove_coin_button.callback = remove_coin_button_callback
        remove_user_button.callback = remove_user_button_callback

        user_manager_view = View()
        user_manager_view.add_item(add_coin_button)
        user_manager_view.add_item(remove_coin_button)
        user_manager_view.add_item(add_warn_button)
        user_manager_view.add_item(remove_user_button)


        await interaction.response.send_message(embed=manager_embed,view=user_manager_view)



@client.tree.command(name='status',description="وضعیت بات و دیتابیس")
@app_commands.default_permissions(administrator=True)
async def status(interaction:Interaction):

    DataBase.cursor.execute("SELECT * FROM table1")
    all_items = DataBase.cursor.fetchall()


    all_coins = 0
    for item in all_items:
        all_coins += item[1]


    all_ads = 0
    for item in all_items:
        all_ads += item[2]


    status_embed = Embed(title='وضعیت بات به شرح زیر میباشد :',description=f"📡 Ping : `{int(client.latency * 1000)}/ms` \n 📟 Server Stats : `🟡` \n 🔌 API Stats : `🟢` \n ",color=0xffffff)


    db_status_embed = Embed(title="وضعیت دیتابیس به شرح زیر میباشد :",color=0x000000)
    db_status_embed.add_field(name=": وضعیت 🔍",value=f"OK",inline=False)
    db_status_embed.add_field(name=":‌ حجم دیتابیس 📦",value="`3kb`",inline=False)
    db_status_embed.add_field(name=": تعداد رکورد ها 🧾",value=f"`{len(all_items)}`",inline=False)

    
    service_stats_embed = Embed(title="وضعیت سرویس به شرح زیر میباشد :",color=0x000000)
    service_stats_embed.add_field(name=":‌ تعداد کاربران 👤",value=len(all_items),inline=False)
    service_stats_embed.add_field(name=":‌ سکه های موجود توی سیستم 💰",value=all_coins,inline=False)
    service_stats_embed.add_field(name=": تعداد کل تبلیغات 🏷️",value=all_ads,inline=False)
    service_stats_embed.add_field(name=": آمار کلی 📊",value="404 Bad request!",inline=False)



    db_stats_button = Button(label="وضعیت دیتابیس",emoji='🗃️',style=ButtonStyle.green)
    service_stats_button = Button(label='وضعیت سرویس',emoji='🧾',style=ButtonStyle.blurple)

    async def db_stats_button_calllback(interaction:Interaction):
        await interaction.response.send_message(embed=db_status_embed)

    async def service_stats_button_callback(interaction:Interaction):
        await interaction.response.send_message(embed=service_stats_embed)


    db_stats_button.callback = db_stats_button_calllback
    service_stats_button.callback = service_stats_button_callback

    status_view = View()
    status_view.add_item(db_stats_button)
    status_view.add_item(service_stats_button)

    await interaction.response.send_message(embed=status_embed,view=status_view)




client.run('Discord app token')
