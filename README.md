# BattleShip
Our final project for infa
# O BattleShip
 BattleShip -- это компьютерная игра, в которой вам нужно собрать все снаряды и уничтожить главную цель. Вы должны, помимо сражения с турелями, после уничтожения которых и выдается один из комплектов боеголовки, защищаться и по возможности также уничтожать корабли злостного врага. BattleShip совершенно бесплатна, что даёт вам доступ ко всем функциям данного приложения. Но вы в любой момент можете поблагодарить разработчиков этой игры разными способами. Их имена:

1. Межнов Андрей, Б02-202
2. Мифтахов Эльдар, Б02-202
3. Кнышов Егор, Б02-202 

Год выпуска игры: 2022

# Требования
Для спокойного запуска игры вам потребуется наличие версии Python 3.9+, который может быть установлен на Windows 8+ или Linux или MacOs. Требований к техническим характеристикам почти не имеется, так как, если на вашем средстве запускаются карты или нарды, то он уже подходит для нашей игры!
Помимо необходимой версии вам потребуются такие библиотеки:
* pygame 
* ffpyplayer
* pymediainfo

О том, как установить данные модули, можно почитать [здесь](https://pypi.org/project/audioplayer/)
А вот один из способов установки модулей с помощью командной строки:
* открываем командную строку
* прописываем следующее:
 > pip install pygame
* нажимаем enter
* ждем загрузку и радуемся жизни)
# Установка игры
У вас есть два способа:
1. Непосредственно с гитхаба производим скачивание всех файлов
2. При наличии git вы можете прописать данную команду и все будет супер
> git clone https://github.com/rinowz/BattleShip
# Запуск игры
Для запуска BattleShip вам необходимо находясь в папке с игрой запустить файл main.py.
После запуска вы попадаете в главное меню, в котором у вас имеется 5 плиток.
# Play
При нажатии на нее вы попадаете в непосредственный бой. 
# Exit 
Клавиша, которая закрывает окно с игрой
# Управление 
После запуска перед вами открыт доступ на управление звездным кораблем:
* Клавиша *W* - движение прямо 
* Клавиша *S* - движение назад
* Клавиша *D* - движение вправо
* Клавиша *A* - движение налево
* Клавиша *Space* - обычный выстрел
* Клавиша *B* - выстрел атомной бомбой
# Игровой процесс
При запуске игры вы погружаетесь в обстановку звездных воинов, у вас имеется свой корабль и самое главное- это Цель. Вам необходимо бороздить по звездным просторам, при этом постоянно отклонясь от метеоритов, пыли и необследованных тел, которые не предоставляют большей опасности, если конечно не попробовать повзаимодействовать с ними(у вас сразу же потеряется часть hp). Помимо более менее безопасных объектов имеются и те, которые находятся в постоянной гонке за вами, они только и наровятся догнать вас и произвести прицельный выстрел, неуклонение от которого повлечет также отнятие части жизни. Но и это еще не все, на главное поле сражения у вас имеются злостные турели, готовые произвести по вам выстрел, в любой подходящий момент, что приведет опять же к снятию урона, но вам то надо не просто уклоняться от всей этой нечести, но и стараться по максимуму производить выстрелы, наиболее значимы они, когда летят в турель. Вам необходимо 3 раза попасть в турель, прежде чем она исчезнет и оставит после себя один из зярядов ядерной бомбы. Таких зарядов вам надо собрать в количестве 3 единиц, то есть поразить 3 турели и при этом выжить во всей этой схватки. И вот наконец-то вам удалось собрать полностью боеголовку и вы как можно быстрее направляетесь к самой большой и неподвижной звезде и совершаете точенчный выстрел этой самой ядерной бомбой и происходит boommmmm!
Обязательно стоит сыграть каждому и как можно больше рассказать друзьям про эту крутую игру, захватывающую дух. А если у вас появились вопросы, то можете обращаться непосредственно к нам или оставлять комментарий на Githab.
