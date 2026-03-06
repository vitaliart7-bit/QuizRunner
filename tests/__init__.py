# limit = int(input())

# maxs = 0

# for n in range(limit//2,limit+1):
#   s = 0
#   d = 1
#   while d *d<=n:
#     if n %d == 0:
#       s += d
#       if n // d != d:
#         s += n // d
#     d+=1
#   if s > maxs:
#     maxs = s
#     ans = n

# print(ans,maxs)










n = int(input())



c = 2

while n % c != 0 and c*c<=n:
  c+=1
  if n %c != 0:
    c = n

print(n//c)
