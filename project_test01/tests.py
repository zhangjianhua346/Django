from django.core.cache import caches

def cache_t():
    # 使用redis缓存
    redis_cache = caches['redis']  # 配置中也要选择redis
    redis_cache.set('zhangsan', '123')
    print(redis_cache.get('zhangsan'))

if __name__ =='__main__':
    cache_t()