public class ThreePrisonersDilemma {

	/*
	 * This Java program models the two-player Prisoner's Dilemma game.
	 * We use the integer "0" to represent cooperation, and "1" to represent
	 * defection.
	 * 
	 * Recall that in the 2-players dilemma, U(DC) > U(CC) > U(DD) > U(CD), where
	 * we give the payoff for the first player in the list. We want the three-player
	 * game
	 * to resemble the 2-player game whenever one player's response is fixed, and we
	 * also want symmetry, so U(CCD) = U(CDC) etc. This gives the unique ordering
	 * 
	 * U(DCC) > U(CCC) > U(DDC) > U(CDC) > U(DDD) > U(CDD)
	 * 
	 * The payoffs for player 1 are given by the following matrix:
	 */

	static int[][][] payoff = {
			{ { 6, 3 }, // payoffs when first and second players cooperate
					{ 3, 0 } }, // payoffs when first player coops, second defects
			{ { 8, 5 }, // payoffs when first player defects, second coops
					{ 5, 2 } } };// payoffs when first and second players defect

	/*
	 * So payoff[i][j][k] represents the payoff to player 1 when the first
	 * player's action is i, the second player's action is j, and the
	 * third player's action is k.
	 * 
	 * In this simulation, triples of players will play each other repeatedly in a
	 * 'match'. A match consists of about 100 rounds, and your score from that match
	 * is the average of the payoffs from each round of that match. For each round,
	 * your
	 * strategy is given a list of the previous plays (so you can remember what your
	 * opponent did) and must compute the next action.
	 */

	abstract class Player {
		// This procedure takes in the number of rounds elapsed so far (n), and
		// the previous plays in the match, and returns the appropriate action.
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			throw new RuntimeException("You need to override the selectAction method.");
		}

		// Used to extract the name of this player class.
		final String name() {
			String result = getClass().getName();
			return result.substring(result.indexOf('$') + 1);
		}
	}

	/* Here are four simple strategies: */

	class NicePlayer extends Player {
		// NicePlayer always cooperates
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 0;
		}
	}

	class NastyPlayer extends Player {
		// NastyPlayer always defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return 1;
		}
	}

	class RandomPlayer extends Player {
		// RandomPlayer randomly picks his action each time
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (Math.random() < 0.5)
				return 0; // cooperates half the time
			else
				return 1; // defects half the time
		}
	}

	class TolerantPlayer extends Player {
		// TolerantPlayer looks at his opponents' histories, and only defects
		// if at least half of the other players' actions have been defects
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int opponentCoop = 0;
			int opponentDefect = 0;
			for (int i = 0; i < n; i++) {
				if (oppHistory1[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			for (int i = 0; i < n; i++) {
				if (oppHistory2[i] == 0)
					opponentCoop = opponentCoop + 1;
				else
					opponentDefect = opponentDefect + 1;
			}
			if (opponentDefect > opponentCoop)
				return 1;
			else
				return 0;
		}
	}

	class FreakyPlayer extends Player {
		// FreakyPlayer determines, at the start of the match,
		// either to always be nice or always be nasty.
		// Note that this class has a non-trivial constructor.
		int action;

		FreakyPlayer() {
			if (Math.random() < 0.5)
				action = 0; // cooperates half the time
			else
				action = 1; // defects half the time
		}

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			return action;
		}
	}

	class T4TPlayer extends Player {
		// Picks a random opponent at each play,
		// and uses the 'tit-for-tat' strategy against them
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0)
				return 0; // cooperate by default
			if (Math.random() < 0.5)
				return oppHistory1[n - 1];
			else
				return oppHistory2[n - 1];
		}
	}

	/* Adding more strategies */

	class SuspiciousT4TPlayer extends Player {
		// instead of T4T which starts with cooperate, this strategy starts with defect
		// by default
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0)
				return 1; // defect by default
			if (oppHistory1[n - 1] == 0 && oppHistory2[n - 1] == 0)
				return 0; // cooperate if both opponents cooperated last round
			else
				return Math.min(oppHistory1[n - 1], oppHistory2[n - 1]); // tit-for-tat
		}
	}

	class T42TPlayer extends Player {
		// Cooperates then plays T4T until opponent defects twice in a row
		// defects, then goes back to playing T4T
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n < 2) {
				return 0; // cooperate by default for first two rounds
			} else {
				// If the opponent defected twice in a row, defect in response
				if (oppHistory1[n - 1] == 1 && oppHistory1[n - 2] == 1) {
					return 1;
				} else {
					return oppHistory1[n - 1]; // copy opponent's previous move
				}
			}
		}
	}

	class ForgivingT4TPlayer extends Player {
		// Cooperates then plays T4T
		// if opponent defects, cooperates for a threshold before switching to defect
		int forgivenessThreshold = 2;

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				return 0; // cooperate by default for first round
			} else {
				// If the opponent defected last round and we have not reached the forgiveness
				// threshold, cooperate this round
				if (oppHistory1[n - 1] == 1 && n <= forgivenessThreshold) {
					return 0;
				} else {
					return oppHistory1[n - 1]; // copy opponent's previous move
				}
			}
		}
	}

	class GrimTriggerPlayer extends Player {
		// Cooperates as long as both players cooperates
		// but defects if other player defects
		boolean defect = false;

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (defect) {
				return 1; // always defect after initial defection
			} else if (n > 0 && oppHistory1[n - 1] == 1) {
				defect = true; // trigger defection if opponent ever defects
				return 1;
			} else {
				return 0; // cooperate otherwise
			}
		}
	}

	class SpitefulPlayer extends Player {
		// Always defects unless both opponents cooperates for at least half the game
		int rounds = 0; // number of rounds played
		int cooperations = 0; // number of times both opponents have cooperated

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0)
				return 0; // cooperate by default
			if (oppHistory1[n - 1] == 1 || oppHistory2[n - 1] == 1) {
				cooperations++;
			}
			rounds++;
			if (cooperations >= rounds / 2)
				return 0; // cooperate if both opponents have cooperated for at least half of the game
			else
				return 1; // always defect
		}
	}

	class PavlovPlayer extends Player {
		// Starts with cooperation
		// Switch to opposite action if low payoff
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				return 0; // start with cooperation
			} else if ((myHistory[n - 1] == oppHistory1[n - 1] && myHistory[n - 1] == 0)
					|| (myHistory[n - 1] != oppHistory1[n - 1] && myHistory[n - 1] == 1)) {
				return 0; // continue with cooperation if last round was successful or I defected
			} else {
				return 1; // defect otherwise
			}
		}
	}

	class GradualPlayer extends Player {
		// Starts with cooperation
		// gradually becomes more likely to defect as game progresses
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				return 0; // cooperate by default for first round
			} else {
				int numDefects = 0;

				// Count the number of times the opponent has defected in the last four rounds
				for (int i = n - 1; i >= n - 4 && i >= 0; i--) {
					if (oppHistory1[i] == 1) {
						numDefects++;
					}
				}

				// If the opponent has defected more than once in the last four rounds, defect
				// this round
				if (numDefects > 1) {
					return 1;
				} else {
					return 0; // otherwise, cooperate
				}
			}
		}
	}

	class AlternateCooperateDefectPlayer extends Player {
		// Alternates between cooperation and defection
		// Starts with cooperation
		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				return 0; // cooperate by default for first round
			} else {
				// Alternate between cooperating and defecting each round
				if (n % 2 == 0) {
					return 1; // defect on even rounds
				} else {
					return 0; // cooperate on odd rounds
				}
			}
		}
	}

	/* Different Combinations of Strategies */

	/**
	 * A player that combines the GrimTrigger and Gradual strategies.
	 */
	class GrimTriggerWithGradualPlayer extends Player {
		// This strategy combines elements of GrimTriggerPlayer and GradualPlayer.
		// It cooperates until the opponent defects, at which point it enters a
		// "grim trigger" mode and defects for a certain number of rounds before
		// reverting back to cooperation.

		private boolean defectMode = false; // Tracks whether the strategy is in defect mode
		private int roundsSinceLastDefect = -1; // Counts the number of rounds since the last defect
		private int threshold = 3; // The number of rounds to defect before reverting back to cooperation

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				return 0; // Cooperate on first move
			}

			// Check if opponent defected last move
			if (oppHistory1[oppHistory1.length - 1] == 1) {
				// If the opponent defected, enter defect mode and reset the rounds counter
				defectMode = true;
				roundsSinceLastDefect = 0;
			}

			// Play according to strategy
			if (defectMode) {
				if (roundsSinceLastDefect >= threshold) {
					// If enough rounds have passed since the last defect, exit defect mode
					defectMode = false;
				} else {
					// Otherwise, increment the rounds counter and continue to defect
					roundsSinceLastDefect++;
				}
				return 1; // Defect if in defect mode
			} else {
				return 0; // Cooperate if not in defect mode
			}
		}
	}

	/**
	 * A player that combines the GrimTrigger and ForgivingT4T strategies.
	 * * Chosen as Soh_QianYi_Player
	 */
	class GrimTriggerWithForgivenessPlayer extends Player {
		// Cooperates first, plays T4T as long as opponent cooperates
		// but defects if other player defects
		// until opponent cooperates twice in a row

		boolean triggered = false; // whether the player has been triggered (GrimTrigger)
		int roundsSinceDefection = 0; // number of rounds since the opponent last defected (ForgivingT4T)

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0)
				return 0; // cooperate by default
			if (triggered)
				return 1; // always defect if triggered (GrimTrigger)
			if (oppHistory1[n - 1] == 0 && oppHistory2[n - 1] == 0)
				return 0; // cooperate if both opponents cooperated last round (ForgivingT4T)
			else if (oppHistory1[n - 1] == 1 || oppHistory2[n - 1] == 1) {
				if (roundsSinceDefection >= 2) {
					triggered = true;
					return 1; // always defect if triggered (GrimTrigger)
				} else {
					roundsSinceDefection++;
					return Math.min(oppHistory1[n - 1], oppHistory2[n - 1]); // tit-for-tat (ForgivingT4T)
				}
			} else {
				roundsSinceDefection = 0;
				return 0; // cooperate if both opponents defected last round (ForgivingT4T)
			}
		}
	}

	/**
	 * A player that combines the Gradual and ForgivingT4T strategies.
	 */
	class GradualWithForgivenessPlayer extends Player {
		// Cooperates first, plays T4T as long as opponent cooperates
		// but defects if other player defects
		// until opponent cooperates twice in a row
		// Also implements Forgiving T4T, by playing cooperatively if the
		// opponent has defected fewer than 'forgivenessThreshold' times in the past
		int forgivenessThreshold = 2; // Threshold for forgiveness
		int cooperateCount = 0; // Count of times opponent cooperated in a row
		int lastAction = 0; // Last action played
		int n = 0; // Round number

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			int oppLastAction = (oppHistory1.length == 0) ? 0 : oppHistory1[oppHistory1.length - 1];

			// Forgiving T4T: plays cooperatively if the opponent has defected fewer than
			// 'forgivenessThreshold' times in the past
			if (oppHistory1.length < forgivenessThreshold
					|| oppHistory1[oppHistory1.length - forgivenessThreshold] == 0) {
				lastAction = 0; // Cooperate
			} else {
				lastAction = oppLastAction; // Play the same as the opponent's last action
			}

			// Gradual: cooperates first, plays T4T as long as opponent cooperates but
			// defects if other player defects
			// until opponent cooperates twice in a row
			if (oppLastAction == 1) { // Opponent cooperated
				cooperateCount = 0;
				return 1; // Cooperate
			} else if (cooperateCount >= 2) { // Opponent defected twice in a row
				cooperateCount = 0;
				return 0; // Defect
			} else { // Opponent defected but less than twice in a row
				cooperateCount++;
				return 1; // Cooperate
			}
		}
	}

	/**
	 * A player that combines the GrimTrigger, Gradual and ForgivingT4T strategies.
	 */
	class GrimTriggerGradualWithForgivenessPlayer extends Player {
		// Cooperates first, then checks opponent histories to determine which strategy
		// to implement.
		// If an opponent defected, it stops using ForgivingT4T and GrimTrigger, and
		// switches to always defecting.
		// If either opponent defects, it switches from Gradual Player to always
		// defecting.
		// If none of the above conditions are met, it cooperates.
		int opponent1LastMove = -1;
		int opponent2LastMove = -1;
		boolean isOpponent1Defected = false;
		boolean isOpponent2Defected = false;
		boolean isGrimTrigger = false;
		boolean isForgiving = false;
		boolean isGradual = false;

		int selectAction(int n, int[] myHistory, int[] oppHistory1, int[] oppHistory2) {
			if (n == 0) {
				isGrimTrigger = true;
				isForgiving = true;
				isGradual = true;
				return 0; // First move: Cooperate
			} else {
				// Check opponent 1 history
				if (opponent1LastMove == 1 && oppHistory1[n - 1] == 0) {
					isOpponent1Defected = true;
				}
				opponent1LastMove = oppHistory1[n - 1];

				// Check opponent 2 history
				if (opponent2LastMove == 1 && oppHistory2[n - 1] == 0) {
					isOpponent2Defected = true;
				}
				opponent2LastMove = oppHistory2[n - 1];

				// Implement Grim Trigger strategy
				if (isGrimTrigger) {
					if (isOpponent1Defected || isOpponent2Defected) {
						isGrimTrigger = false;
						return 1;
					} else {
						return 0;
					}
				}

				// Implement Forgiving T4T strategy
				if (isForgiving) {
					if (isOpponent1Defected || isOpponent2Defected) {
						isForgiving = false;
						return 1;
					} else {
						return opponent1LastMove == 0 && opponent2LastMove == 0 ? 0 : 1;
					}
				}

				// Implement Gradual Player strategy
				if (isGradual) {
					if (opponent1LastMove == 1 || opponent2LastMove == 1) {
						isGradual = false;
						return 1;
					} else {
						return 0;
					}
				}

				// If none of the above strategies are active, cooperate
				return 0;
			}
		}
	}

	/*
	 * In our tournament, each pair of strategies will play one match against each
	 * other.
	 * This procedure simulates a single match and returns the scores.
	 */
	float[] scoresOfMatch(Player A, Player B, Player C, int rounds) {
		int[] HistoryA = new int[0], HistoryB = new int[0], HistoryC = new int[0];
		float ScoreA = 0, ScoreB = 0, ScoreC = 0;

		for (int i = 0; i < rounds; i++) {
			int PlayA = A.selectAction(i, HistoryA, HistoryB, HistoryC);
			int PlayB = B.selectAction(i, HistoryB, HistoryC, HistoryA);
			int PlayC = C.selectAction(i, HistoryC, HistoryA, HistoryB);
			ScoreA = ScoreA + payoff[PlayA][PlayB][PlayC];
			ScoreB = ScoreB + payoff[PlayB][PlayC][PlayA];
			ScoreC = ScoreC + payoff[PlayC][PlayA][PlayB];
			HistoryA = extendIntArray(HistoryA, PlayA);
			HistoryB = extendIntArray(HistoryB, PlayB);
			HistoryC = extendIntArray(HistoryC, PlayC);
		}
		float[] result = { ScoreA / rounds, ScoreB / rounds, ScoreC / rounds };
		return result;
	}

	// This is a helper function needed by scoresOfMatch.
	int[] extendIntArray(int[] arr, int next) {
		int[] result = new int[arr.length + 1];
		for (int i = 0; i < arr.length; i++) {
			result[i] = arr[i];
		}
		result[result.length - 1] = next;
		return result;
	}

	/*
	 * The procedure makePlayer is used to reset each of the Players
	 * (strategies) in between matches. When you add your own strategy,
	 * you will need to add a new entry to makePlayer, and change numPlayers.
	 */

	int numPlayers = 16;

	Player makePlayer(int which) {
		switch (which) {
			case 0:
				return new NicePlayer();
			case 1:
				return new NastyPlayer();
			case 2:
				return new TolerantPlayer();
			case 3:
				return new T4TPlayer();
			case 4:
				return new SuspiciousT4TPlayer();
			case 5:
				return new T42TPlayer();
			case 6:
				return new ForgivingT4TPlayer();
			case 7:
				return new GrimTriggerPlayer();
			case 8:
				return new SpitefulPlayer();
			case 9:
				return new PavlovPlayer();
			case 10:
				return new GradualPlayer();
			case 11:
				return new AlternateCooperateDefectPlayer();
			case 12:
				return new GrimTriggerWithGradualPlayer();
			case 13:
				return new GrimTriggerWithForgivenessPlayer(); // chosen as Soh_QianYi_Player
			case 14:
				return new GradualWithForgivenessPlayer();
			case 15:
				return new GrimTriggerGradualWithForgivenessPlayer();

		}
		throw new RuntimeException("Bad argument passed to makePlayer");
	}

	/* Finally, the remaining code actually runs the tournament. */

	public static void main(String[] args) {
		ThreePrisonersDilemma instance = new ThreePrisonersDilemma();
		instance.runTournament();
	}

	boolean verbose = true; // set verbose = false if you get too much text output

	void runTournament() {
		float[] totalScore = new float[numPlayers];

		// This loop plays each triple of players against each other.
		// Note that we include duplicates: two copies of your strategy will play once
		// against each other strategy, and three copies of your strategy will play
		// once.

		for (int i = 0; i < numPlayers; i++)
			for (int j = i; j < numPlayers; j++)
				for (int k = j; k < numPlayers; k++) {

					Player A = makePlayer(i); // Create a fresh copy of each player
					Player B = makePlayer(j);
					Player C = makePlayer(k);
					int rounds = 90 + (int) Math.rint(20 * Math.random()); // Between 90 and 110 rounds
					float[] matchResults = scoresOfMatch(A, B, C, rounds); // Run match
					totalScore[i] = totalScore[i] + matchResults[0];
					totalScore[j] = totalScore[j] + matchResults[1];
					totalScore[k] = totalScore[k] + matchResults[2];
					if (verbose)
						System.out.println(A.name() + " scored " + matchResults[0] +
								" points, " + B.name() + " scored " + matchResults[1] +
								" points, and " + C.name() + " scored " + matchResults[2] + " points.");
				}
		int[] sortedOrder = new int[numPlayers];
		// This loop sorts the players by their score.
		for (int i = 0; i < numPlayers; i++) {
			int j = i - 1;
			for (; j >= 0; j--) {
				if (totalScore[i] > totalScore[sortedOrder[j]])
					sortedOrder[j + 1] = sortedOrder[j];
				else
					break;
			}
			sortedOrder[j + 1] = i;
		}

		// Finally, print out the sorted results.
		if (verbose)
			System.out.println();
		System.out.println("Tournament Results");
		for (int i = 0; i < numPlayers; i++)
			System.out.println(makePlayer(sortedOrder[i]).name() + ": "
					+ totalScore[sortedOrder[i]] + " points.");

	} // end of runTournament()

} // end of class PrisonersDilemma
