import asyncio
import pytest
from connect import standalone_reconnect
from connect import no_recconect_task_manager
from connect import reconnect_task_manager
from connect import test4_task_manager
#reconnect works
def test_standalone_reconnect():
    asyncio.get_event_loop().run_until_complete(standalone_reconnect())


# Reconnect works automatically but only for short time and ws.send sends all unsended messages;
def test_no_reconnect():
    asyncio.run(no_recconect_task_manager())

#This shit does not work, i dont know why.
#Recconnect works, but sender know nothing about that;
#Need to think about flow
def test_reconnect_manager():
    asyncio.run(reconnect_task_manager())


# IT WORKS!
def test_strongest_socket():
    asyncio.run(test4_task_manager())

