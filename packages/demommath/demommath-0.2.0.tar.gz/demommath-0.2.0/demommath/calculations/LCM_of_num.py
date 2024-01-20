def lcm(a, b, c):
 
  max_num = max(a, b, c)
  lcm = max_num

  while True:
    if lcm % a == 0 and lcm % b == 0 and lcm % c == 0:
      break
    lcm += max_num

  return lcm