import discord
from tipper.tipper import *

client = discord.Client()


@client.event
async def on_message(message):
    #make sure bot doesnt reply to himself
    if message.author == client.user:
        return

    if message.content.startswith('/price'):
        msg = getPriceMSG()
        return await client.send_message(message.channel,msg)


    if message.content.startswith('/help'):
        helpmsg = "/info** - Project info\n**/botinfo** - bot contact\n**/deposit** - shows your deposit address\n**/balance ** - shows your balance\n**/price** - price DASHP\n**/tip** [user] [amount] - tips another user coins\n**/rain** [amount] - send coin for all users.\n**/withdraw** [amount] [address] - withdraws funds to an external address\n/donate [amount] - donation to bot developer**\n"
        return await client.send_message(message.channel,helpmsg)

    if message.content.startswith('/botinfo'):
        botinfo = "Hello I m a wallet and tipbot official from the DashPlatinum DASHP Use:\n**/deposit** to participate in the rains or\n**/help** to see all commands\nto your personalized bot from any currency send a message to discord @Feliciox#2656"
        return await client.send_message(message.channel,botinfo)

    if message.content.startswith('/info'):
        infomsg = "```Coin Name DashPlatinum\nTicket DASHP\nMax Supply 19700000\nBlock Time 120 seconds\nMasternode Colateral\n3000 DASHP  =  80% of blocks\nRewards Per Block\n0004 - 10000 = 1.10 DASHP\n14400 - 28799 = 1.70 DASHP\n28800 - 43199 = 2.60 DASHP\n43200 - 57599 = 2.90 DASHP\n57600 - 172799 = 5.10 DASHP\n172800 - 345599 = 4.59 DASHP\n345600 - 518399 = 4.05 DASHP\n518400 - 604799 = 3.64 DASHP\n604800 - forward = 3.28 DASHP\n```"
        return await client.send_message(message.channel,infomsg)

    if message.content.startswith('/deposit') or message.content.startswith('/addr'):

        account = message.author.id
        print(type(account))
        address = getAddress(account)

        msg = '{0.author.mention}, your address is \n```%s```'.format(message)%address
        return await client.send_message(message.channel,msg)

    if message.content.startswith('/balance stake'): #0conf balance
        account = message.author.id
        balance = getBalance(account,0)
        msg = '{0.author.mention}, you have %1.8f DASHP, including stake'.format(message)%balance
        return await client.send_message(message.channel,msg)

    if message.content.startswith('/balance'):
        account = message.author.id
        print(account)
        balance = getBalance(account)
        #price = getPrice(float(balance))
#        msg = '{0.author.mention}, you have  %f DASHP'.format(message)%(balance)
        msg = '{0.author.mention}, you have  ``%1.8f DASHP``'.format(message)%(balance)
        return await client.send_message(message.channel,msg)

    if message.content.startswith('/tip '):
        tipper = message.author.id
        content = message.content.split()[1:]
        toTipMention = content[0]
        toTip = toTipMention.replace('<@','').replace('>','') #remove <@> from ID
        amount = content[1]

        #catching errors
        if not toTipMention[:2]=='<@':
            return await client.send_message(message.channel,"{0.author.mention}, invalid account.".format(message))
        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            tip(tipper,toTip,amount)
            #price = getPrice(float(amount))
            return await client.send_message(message.channel,"{0.author.mention} has tipped %f DASHP.".format(message)%(toTipMention,amount))
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('/withdraw '):
        account = message.author.id
        amount = message.content.split()[1]
        address = message.content.split()[2]

        #catching errors again
        if not validateAddress(address):
            return await client.send_message(message.channel,"{0.author.mention}, invalid address.".format(message))

        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            txid = withdraw(account,address,amount)
            return await client.send_message(message.channel,"{0.author.mention}, withdrawal complete, TXID %s".format(message)%txid)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('/rain '):
        account = message.author.id
        amount = float(message.content.split()[1])

        if amount < 0.01:
            return await client.send_message(message.channel,"{0.author.mention}, the amount must be bigger than 0.01 DASHP".format(message))
        #catching errors again
        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            eachtip = rain(account,amount) #the function returns each individual tip amount so this just makes it easier
            #return await client.send_message(message.channel,"{0.author.mention} has tipped  %1.8f dashp to everyone on this server!".format(message)%eachtip)
            return await client.send_message(message.channel,"{0.author.mention} has tipped  %1.8f DASHP to @everyone on this server!".format(message)% eachtip)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))


    if message.content.startswith('/donate'):
        account = message.author.id
        address = "LUF2RoCukvBSMZmL1cXAXsJT6EGE8ViKQT"#LNO marketing donation account
        amount = message.content.split()[1]

        #catching errors
        if not validateAddress(address):
            return await client.send_message(message.channel,"{0.author.mention}, invalid address.".format(message))

        try:
            amount = float(amount)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, invalid amount.".format(message))

        try:
            txid = withdraw(account,address,amount)
            return await client.send_message(message.channel,"{0.author.mention}, Thank you for your donation! TXID: %s".format(message)%txid)
        except ValueError:
            return await client.send_message(message.channel,"{0.author.mention}, insufficient balance.".format(message))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')



client.run('NTUxMjQ0MDk0Mzc1MTk4NzI4.XOR6bg.vRq3Sa8byY3rmutG5II4-i30F14')
