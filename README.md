# roll20_scrapper
Parser\scrapper for roll20, without rolls, only history remains 

------------------------

first u need cookie and link, this actually do work

#### -How to get link?
go on  roll20 -> Games -> Choose game you want to parse -> content -> Chat Archive -> last (in up left corner) 
It`s your link, copy and paste in code. shud looks like this https://app.roll20.net/campaigns/chatarchive/########/?p=227&onePage=&hidewhispers=&hiderollresults="
where "/########/" id of campain, "?p=227" 227 numbers of pages

#### -How to get cookie?
Open link, open dev tools on network, reload tab, watch 1st request(he should be simular to link), right click on req, change and resend, find cookie in new opened window, highlight value, right click and copy. 

rack.session=****************************************************; gdpr_accepts_cookies=true; roll20tempauth=48; __stripe_mid=***********************; __stripe_mid=**************************************; __stripe_sid=**************************************;
yes there x2 __stripe_mid, idk why, it doesnt matter anyway 

------------------------

u can modify it like adding avatar, PlayerID and many other things,
just add it here in code:
                dataToWrite.append(timestamp_to_datetime(value['.priority']))
                dataToWrite.append(value['who'])
                dataToWrite.append(value['content'])
                dataToWrite.append(value['avatar']) // like this

and dont forghet add new field: 
      writer.writerow(['Timestamp', 'Name', 'Content', 'Avatar'])

Example of parse:

Timestamp,Name,Content
2022-03-12 15:13:12,руки не мои,𐐘 𐐘 𐐘
2022-03-12 15:13:25,руки не мои,ඞ ඞ ඞ
2022-03-13 18:32:02,Кира,Превращаться и надевать костюм амогуса


If something doesnt work go to issues and send letter :)
