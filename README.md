# block-puzzle-solver
you know you'r down when you think of nothing but making a block puzzle solver ,
  and not in any normal time but in the middle of a law lecture.

the game is all about putting block puzzles in their desired slots as shown in the following illustrations
- ![#f03c15](https://placehold.co/15x15/f03c15/f03c15.png) `red means the desired place for the puzzle`
- ![#f03c15](https://placehold.co/15x15/A020F0/A020F0.png) `purple is obviously the puzzle itself`
- ![#f03c15](https://placehold.co/15x15/008000/008000.png) `and green is the rows or columns to be vanished`

`first movement`

![462570045_755554623412534_1102835430539069030_n](https://github.com/user-attachments/assets/f23a5f2b-d55f-4aeb-beb6-ce88ebe8d616)

`socond movement`

![462552776_1226505021943485_4525084634888960684_n](https://github.com/user-attachments/assets/0cf9f862-18db-4001-b0a2-10e34a78dce0)

`result of socond movement`

![462553583_1541789136466152_5941599449231968065_n](https://github.com/user-attachments/assets/18bc61a8-1a61-41ec-b56e-6bdbd92964f8)

`third movement`

![465771492_1290445515471018_8647355838806321887_n](https://github.com/user-attachments/assets/8a55067f-129f-44a0-bd22-cf097d227b20)

`result of third movement`

![462547273_2449451338727574_7918360941791976671_n](https://github.com/user-attachments/assets/1c420e04-a412-4e52-ab69-7fade63a9586)

`finally the ending map with new puzzles respawned`

![462541880_544762258514597_3954476601817793683_n](https://github.com/user-attachments/assets/fa3c50b0-6dca-4d98-a053-f67a2c7de4f1)

unfortunately the map could get locked down that there is no way you can sort the puzzles in any sequence so that the puzzles matches the free slots in the map , and this happens due to placing the puzzles in a wrong sequence as in the following illustration:

![462551117_1074106517779050_2056490610070259805_n](https://github.com/user-attachments/assets/b33a771c-b621-4145-9a96-d5f6b20898c1)

for this block puzzle solver you can think of the map as a nested array where every row e.g (nestedArray[i]) has 0s and 1s,
1 = obsticle or a non-free slot
0 = free slot
map = [
  [0,1,1,1],
  [0,0,0,1]
]
the same goes with the puzzle , each puzzle must has rows and each row has it's own 1s & 0s
1 = part of the puzzle
0 = not part of the puzzle

`note : you need to complete the puzzle's rows with zeros because every row must has the same length`

`example 1`

puzzle = [

  [1,0,0],

  [1,1,1]

]

![462567415_3002122779939469_2461848425688110165_n](https://github.com/user-attachments/assets/0b3d53fe-88f0-4f50-a7b4-cd196b49b3a1)

`example 2`

puzzle = [

  [0,1,0],

  [1,1,1]

]

![462549900_1216366036083027_7347744888436743083_n](https://github.com/user-attachments/assets/3d40b6c2-88f6-4944-b309-13e5c0a1d39a)

general explanation for how this block puzzle solver workes in three steps:

`1st step`

- invert the map to free-sloted map where every 1 is a free slot rather than an obsticle and every 0 is and obsticle rather than a free slot

`2nd step`

- search for solutions for each individual puzzle

`3rd and final step`

- combine solutions of puzzles into one combined solution by recursion

the idea behind the algorithm used in this repo , is inspired from the game called "block blast" , hope you value the effort put in this code :)
