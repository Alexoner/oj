/*
 * Longest Consecutive Sequence
 * Given an unsorted array of integers, find the length of the longest
 * consecutive elements sequence.
 *
 * For example, Given [100, 4, 200, 1, 3, 2], the longest consecutive
 * elements sequence is [1, 2, 3, 4]. Return its length: 4.
 *
 * Your algorithm should run in O(n) complexity.
 *
 *
 * ALgorithm:
 * Graph path problem, do a DEPTH-FIRST SEARCH with HASH TABLE to store elements for
 * accessing them in O(1) time.
 */


import java.util.Hashtable;

public class LongestConsecutive {

    static public int longestConsecutive(int[] num) {
        Hashtable<Integer, Integer> table = new Hashtable<Integer, Integer>();
        int curr = 1, length = 0, left, right;
        for (int i : num) {
            table.put(i, 1);
        }

        for (int e : num) {
            left = e - 1;
            right = e + 1;
            length = 1;

            while (table.containsKey(left)) {
                length++;
                table.remove(left);
                left--;
            }

            while (table.containsKey(right)) {
                length++;
                table.remove(right);
                right++;
            }

            if (length > curr) {
                curr = length;
            }
        }

        return curr;
    }

    public static void main(String[] args) {
        System.out.println(LongestConsecutive.longestConsecutive(new int[] { 100, 4, 200, 1, 3, 2 }));
    }
}
