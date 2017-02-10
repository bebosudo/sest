TODO:
-----

Requirements to develop.

Do not change the order or insert new reqs in the middle of the list.

1. ~~set up the email sending module.~~

1. ~~save every field as a string, and save (inside the channel class) the `encoding' to use to recover the value from that string.~~

1. ~~let the user define different triggering actions for each channel~~ <br />
*have to finish writing some tests*

1. ~~redefine the Record.save() method, by placing the actions to be triggered there~~

5. set up a cron job that every X (5 mins? 10?) sends a request on a special View that scans the whole DB of Channels, and compares the last_update field with the update_interval (it still has to be created) and trigger a special trigger action the user chose for that channel to signal inactivity --> to be done with the Periodic Tasks from celery.

1. **[WEB]** make the user choose which kind of field encoding to use from a defined list for each field of the channel.

1. ~~check whether the values are of the correct type at the saving time.~~

1. ~~check (with a test) that requests with wrong field names (instead of field1, .., field43) are not accepted by the upload view.~~

1. ~~check (with a test) that fields (keys) without values (field1=& ...) are not accepted by the upload view.~~

10. ~~At the saving time, check that the values are consistent with their field encoding.~~

1. **[WEB]** add an (optional) name to each field (could be placed inside the FieldEncoding, since it has to be unique for every field.. maybe the name can be changed from FieldEncoding to something more generic)

1. ~~create tests for the ConditionAndReaction class~~

1. **[WEB/secondary req.]** validate the email the user inserts, by making sure that he really owns that address.
Cornercase: if the user already certified their registration email, there's no need to ask to certificate it again.

1. **[WEB]** translations.

15. ~~Make sure that there are no more than one FieldEncoding object for each field_no (there should be something like a composite pk on the channel and the field_no).~~

1. update the secret_settings_example.py file ~~(and rename them secret_settings{,_example}.py)~~

1. check and test what happens when many 'fieldX' with the same name (and diff values?) are passed to the upload view to be saved. --> this shouldn't happen, since the field should overwrite each other when are read by django.

1. ~~https://www.peterbe.com/plog/interesting-casting-in-python~~

1. -

20. -
