from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone

from django.utils.text import slugify
from django.template.defaultfilters import slugify

from taggit.managers import TaggableManager
from taggit.models import TagBase

from unidecode import unidecode


class PublishedManager(models.Manager):
    """
    Own model manager.
    Only published posts will be displayed.
    Собственный менеджер модели.
    Будут отображаться только опубликованные посты.
    """
    def get_queryset(self):
        """
        Returns a QuerySet filtered by status = 'published'. A QuerySet with
        posted posts will be returned.
        Возвращает QuerySet с фильтром по status='published'. Будет возвращен
        QuerySet с опубликованными постами.
        """
        return super(PublishedManager, self) \
            .get_queryset() \
            .filter(status='published')


class Category(models.Model):
    """
    Model data categories blog publications.
    Модель данных категорий постов блога.
    """
    category = models.CharField(verbose_name='Категория',
                                max_length=15,
                                blank=False)
    slug = models.SlugField(max_length=250,
                            blank=True,
                            unique='category')
    category_manager = models.Manager()

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        db_table = 'category'

    def __str__(self):
        return self.category



    def save(self, *args, **kwargs):
        """
        Overridden standard save() function. Serves for automatic slug
        creation. If the post has no slug, the slugify() function
        automatically forms it from the passed header, after which
        the post object is saved.
        Переопределенная стандартная функция save(). Служит для автоматического
        формирования slug. Если у поста нет слага, функция slugify()
        автоматически формирует его из переданного заголовка, после чего
        происходит сохранение объекта поста.
        """
        if not self.slug:
            self.slug = slugify(unidecode(self.category))
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        The function generates direct links.
        Функция формирует прямые ссылки.
        """
        return reverse('publications:post_category',
                       args=[self.category, self.slug])


class Post(models.Model):
    """
    Data model for blog posts.
    Модель данных для постов блога.
    """
    STATUS_CHOICES = (
        ('draft', 'черновик'),
        ('published', 'опубликовано')
    )

    title = models.CharField(verbose_name='Заголовок поста', max_length=250)
    slug = models.SlugField(max_length=250,
                            blank=True,
                            unique_for_date='date_published')
    author = models.ForeignKey(User,
                               verbose_name='Автор поста',
                               on_delete=models.CASCADE,
                               related_name='publications_posts')
    category = models.ForeignKey(Category,
                                 verbose_name='Категория',
                                 on_delete=models.CASCADE,
                                 related_name='publications_category')
    body = models.TextField(verbose_name='Содержание поста')
    date_published = models.DateTimeField(verbose_name='Дата публикации поста',
                                          default=timezone.now)
    created = models.DateTimeField(verbose_name='Дата написания поста',
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата обновления поста',
                                   auto_now=True)
    status = models.CharField(verbose_name='Статус',
                              max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    # Model manager
    # Менеджер модели
    published = PublishedManager()

    # Manager tags
    # Менеджер тегов
    tags = TaggableManager()

    class Meta:
        ordering = ('-date_published',)
        verbose_name = 'пост'
        verbose_name_plural = 'посты'
        db_table = 'posts'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Overridden standard save() function. Serves for automatic slug
        creation. If the post has no slug, the slugify() function
        automatically forms it from the passed header, after which
        the post object is saved.
        Переопределенная стандартная функция save(). Служит для автоматического
        формирования slug. Если у поста нет слага, функция slugify()
        автоматически формирует его из переданного заголовка, после чего
        происходит сохранение объекта поста.
        """
        if not self.slug:
            self.slug = slugify(unidecode(self.title))
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        """
        The function generates direct links.
        Функция формирует прямые ссылки.
        """
        return reverse('publications:post_detail',
                       args=[self.date_published.year,
                             self.date_published.month,
                             self.date_published.day,
                             self.slug])


class Comment(models.Model):
    """
    Comment model
    Модель комментариев
    """
    post = models.ForeignKey(Post,
                             verbose_name='Пост',
                             on_delete=models.CASCADE,
                             related_name='publications_comments')
    author = models.CharField(verbose_name='Имя', max_length=80)
    email = models.EmailField(verbose_name='e-mail')
    body = models.TextField(verbose_name='Коментарий')
    created = models.DateTimeField(verbose_name='Дата создания комментария',
                                   auto_now_add=True)
    updated = models.DateTimeField(verbose_name='Дата изменения комментария',
                                   auto_now=True)
    moderation = models.BooleanField(verbose_name='Модерация', default=True)

    class Meta:
        ordering = ('created',)
        verbose_name = 'Коментарий'
        verbose_name_plural = 'Коментарии'
        db_table = 'comments'

    def __str__(self):
        """
        The method returns the display of the object in a understandable way.
        Метод возвращает отображение объекта понятном виде.
        """
        return 'Коментарий от {} на {}'.format(self.author, self.post)
