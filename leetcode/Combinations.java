/*
 * Combinations
 *
 * Given two integers n and k, return all possible combinations of k numbers out of 1 ... n.
 *
 * For example,
 * If n = 4 and k = 2, a solution is:
 *
 * [
 *  [2,4],
 *  [3,4],
 *  [2,3],
 *  [1,2],
 *  [1,3],
 *  [1,4],
 * ]
 *
 * =================================================================================
 *
 * The problem of generating permutations and combinations can be transformed into
 * generating k-DIGITAL NUMBERS from n candidate numbers in a DIGITWISE way. We start with
 * the lowest one. At each pass, do ADDITION ARITHMETIC by 1 to the right-most digit with carry
 * added to left, along way to the highest one.
 * The difference with combination is that the sequence generated at each round must be increasing.
 */


import java.util.ArrayList;
import java.util.List;

public class Combinations {

	public List<List<Integer>> combineDFS(int n, int k) {
		List<List<Integer>> result = new ArrayList<List<Integer>>();
		List<Integer> combination = new ArrayList<Integer>();
		for (int i = 1; i + k <= n; ++i) {

		}
		return result;
	}

	public List<List<Integer>> combine(int n, int k) {
		List<List<Integer>> combinations = new ArrayList<List<Integer>>();
		// n == k is acceptable
		if (n < k || k <= 0 || n <= 0) {
			if (k == 0) {
				// Generate empty set,necessary by definition
				return combinations;
			}
			return null;
		}
		int icur = 0;
		List<Integer> combination = new ArrayList<Integer>();
		for (int i = 0; i < k; i++) {
			combination.add(-1);
		}

		while (icur >= 0) {
			if (icur == k) {
				// filled all slot,seeking next combination solution
				icur--;
			}
			if (combination.get(icur) == -1) {
				// fill next slot
				if (icur > 0) {
					combination.set(icur, combination.get(icur - 1) + 1);
				} else {
					// Fill in the 1st slot first time.
					combination.set(icur, 1);
				}
				// icur++;
			} else {
				// increase the index on current slot by 1 to find next combination
				combination.set(icur, combination.get(icur) + 1);
			}

			// validation
			if (combination.get(icur) > n) {
				combination.set(icur, -1);
				// pop out of the stack
				icur--;
				continue;
			} else {
				// push into the stack
				icur++;
			}

			if (icur == k) {
				// filled all slot,generating a combination
				// We need to copy a List,not adding this list.
				combinations.add(new ArrayList<Integer>(combination));
			}
		}
		return combinations;
	}

	public static void main(String[] args) {
		Combinations sol = new Combinations();
		List<List<Integer>> sols = sol.combine(5, 2);
		System.out.println("Solutions are");
		System.out.println(sols);
	}
}
