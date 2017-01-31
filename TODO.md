TODO:
-----

1. ~~set up the email sending module.~~

1. save every field as a string, and save (inside the channel class) the `encoding' to use to recover the value from that string.
    * perform the needed checks of consistency before accepting and saving the objects to the DB.

1. redefine the Record.save() method, by placing the actions to be triggered there

1. let the user define different triggering actions for each channel

1. set up a cron job that every X (5 mins? 10?) sends a request on a special View that scans the whole DB of Channels, and compares the last_update field with the update_interval (it still has to be created) and trigger a special trigger action the user chose for that channel to signal inactivity
