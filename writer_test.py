from app import writer

maze = [[13, 3, 13, 3],
        [11, 12, 3, 10],
        [8, 3, 12, 2],
        [14, 12, 7, 14]]
entry = (0, 0)
exit_port = (19, 15)
path = "SWESENSWSSENEEENNESSSEES"
try:
    writer.output_maze("out_maze.txt", maze, entry, exit_port, path)
except OSError as e:
    print(f"Error: {e}")
