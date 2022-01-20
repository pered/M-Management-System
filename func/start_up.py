import logging
from typing import Tuple, Optional

from telegram import Update, Chat, ChatMember, ParseMode, ChatMemberUpdated
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    ChatMemberHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


updater = Updater("TOKEN")