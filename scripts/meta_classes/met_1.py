class Meta(type):
    def __str__(self):
        return 'weird thing'


class Hello(metaclass=Meta):
    pass


print(Hello)
