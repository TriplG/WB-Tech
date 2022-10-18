# Тестовое задание стажиров на Backend

### Мною были выполнены все 8 пунктов задания(само задание смотреть ниже), в качестве субд использовался PostgreSQL, все зависимости находятся в файле requirements.txt

## Задание
Реализовать backend часть для блога в виде сервиса с REST API. Приложение должно
позволять:
1. Регистрироваться новым пользователям и выполнять вход существующих.
2. Авторизованным пользователям создавать посты. Пост имеет заголовок и текст
поста.
3. Просматривать список пользователей с возможностью сортировки по количеству
постов.
4. Просматривать список постов других пользователей, отсортированный по дате
создания, сначала свежие.
5. Авторизованным пользователям подписываться и отписываться на посты других
пользователей.
6. Авторизованным пользователям формировать ленту из постов пользователей, на
которые была осуществлена подписка. В ленту попадают новые посты
пользователей после выполнения подписки. Сортировка по дате создания поста,
сначала свежие. Список постов отдается страницами по 10шт.
7. Авторизованным пользователям помечать посты в ленте как прочитанные и
выполнять фильтрацию постов по данному признаку.
8. Администратору управлять пользователями и контентом средствами Django admin.