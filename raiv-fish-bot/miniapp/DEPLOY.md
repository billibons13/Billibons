# Публикация витрины RAIV FISH на Netlify

Сайт: https://raiv-fish-shop.netlify.app (Netlify project id 88c53092-cb0b-4b4e-8525-798262c66389).
Файлы сайта — эта папка: index.html, img/, netlify.toml (index.html собирается командой `python3 generate_miniapp.py`).

Задание для Claude на компьютере владельца:
1. git clone https://github.com/billibons13/Billibons && git checkout claude/blissful-tesla-9xox1x
2. cd raiv-fish-bot/miniapp
3. Опубликовать папку в существующий проект (не создавать новый):
   npx -y netlify-cli deploy --prod --dir . --site 88c53092-cb0b-4b4e-8525-798262c66389
   (при первом запуске netlify-cli попросит войти в аккаунт Netlify в браузере)
4. Проверить, что https://raiv-fish-shop.netlify.app/ и /img/b5.jpg открываются.
5. Ничего другого не менять: бота в Make обновит облачная сессия Claude после ответа «готово».
