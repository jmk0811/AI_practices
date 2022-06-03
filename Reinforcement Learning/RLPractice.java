import java.util.Random;

public class RLPractice {
	
	public static final int NUM_ROWS = 2; // Number of rows in the grid world
	public static final int NUM_COLS = 4; // Number of columns in the grid world
	public static final int NUM_ACTIONS = 4; // Four possible moves in each cell
	
	public static final double DISCOUNT = 0.9; // Discount factor.
	public static final double EPSILON = 0.01; // Exploration parameter.
	public static final double SUCCESS_FACTOR = 0.91; // Probability of success 
	
	double P[][][]; // Transition probabilities
	double R[][];   // Rewards
	double V[];     // Value function
	double Q[][];   // Action-value function
	int policy[];   // Deterministic policy
	// double policy[][]; // For stochastic policy
	
	double cumReward;
	double curReward;
	
	int curState;
	int nStates = NUM_ROWS * NUM_COLS; // Row-major indexing of the grid cells
	int curStep;
	int step = 1000000;
	
	public RLPractice() {
		init();
	}
	
	public void init() {
		Random rnd = new Random();
		P = new double[NUM_ACTIONS][nStates][nStates]; // action-orgState-dstState
		R = new double[NUM_ACTIONS][nStates];
		V = new double[nStates];
		Q = new double[nStates][NUM_ACTIONS];
		policy = new int[nStates];
		// policy = new double[nStates][NUM_ACTIONS];  // For stochastic policy
		
		for (int i = 0; i < NUM_ACTIONS; i++) { 
			for (int j = 0; j < nStates; j++) { // from state
				double reward = (rnd.nextInt(10) - 6) * 2;
				int up = j - RLPractice.NUM_COLS;
				if (up < 0)
					up = j + RLPractice.NUM_COLS * (RLPractice.NUM_ROWS - 1);
				int down = j + RLPractice.NUM_COLS;
				if (down >= nStates)
					down = j - RLPractice.NUM_COLS * (RLPractice.NUM_ROWS - 1);
				int curCol = j % RLPractice.NUM_COLS;
				int left = curCol == 0 ? j + NUM_COLS - 1 : j - 1;
				int right = curCol == RLPractice.NUM_COLS - 1 ? j - NUM_COLS + 1 : j + 1;

				R[i][j] = reward; // rewards are independent of actions
				for (int k = 0; k < nStates; k++) { // destination state
					switch (i) {
					case 0: // up
						if (k == up)
							P[i][j][k] = RLPractice.SUCCESS_FACTOR;
						else if (k == left || k == right || k == down)
							P[i][j][k] = (1 - RLPractice.SUCCESS_FACTOR) / 3;
						break;
					case 1: // right
						if (k == right)
							P[i][j][k] = RLPractice.SUCCESS_FACTOR;
						else if (k == left || k == up || k == down)
							P[i][j][k] = (1 - RLPractice.SUCCESS_FACTOR) / 3;
						break;
					case 2: // left
						if (k == left)
							P[i][j][k] = RLPractice.SUCCESS_FACTOR;
						else if (k == up || k == right || k == down)
							P[i][j][k] = (1 - RLPractice.SUCCESS_FACTOR) / 3;
						break;
					case 3: // down
						if (k == down)
							P[i][j][k] = RLPractice.SUCCESS_FACTOR;
						else if (k == left || k == right || k == up)
							P[i][j][k] = (1 - RLPractice.SUCCESS_FACTOR) / 3;
						break;
					}
					// P[i][j][k] = 0;
				}
			}
		}

		curState = rnd.nextInt(nStates);
		curStep = 0;
	}

	public void valueIteration() { 
		// initialize policy
		for (int i = 0; i < nStates; i++) {
			policy[i] = 0;
		}
		
		// Arbitrarily initialize V
		for (int j = 0; j < nStates; j++) {
			V[j] = 0;
		}

		// Repeat until the error becomes sufficiently small
		for (int z = 0; z < 1000; z++) {
			double err = 0.0;
			for (int j = 0; j < nStates; j++) { // from state
				// v <= V(s)
				double v = V[j];
				
				double max = 0;
				for (int i = 0; i < NUM_ACTIONS; i++) { // for all actions
					double sum = 0;
					for (int k = 0; k < nStates; k++) { // destination state
						sum += P[i][j][k] * (R[i][j] + DISCOUNT * V[k]);
					}
					max = max(max, sum);
				}
				
				// V(s) <= max_a( ... )
				V[j] = max;
				
				// error <= max(error, |v - V(s)|)
				double newErr = Math.abs(v - V[j]);
				err = max(err, newErr);
			}
			/*
			 * uncomment the bottom line to print the error for each step
			 * 					|
			 * 					|
			 * 					V
			 */
			//System.out.println("Step: " + (z + 1) + ", Error: " + err);
		}
		
		
		// Policy Calculation
		for (int j = 0; j < nStates; j++) { // from state
			double max = 0;
			for (int i = 0; i < NUM_ACTIONS; i++) { // for all actions
				double sum = 0;
				for (int k = 0; k < nStates; k++) { // destination state
					sum += P[i][j][k] * (R[i][j] + DISCOUNT * V[k]);
				}
				if (max < sum) {
					max = sum;
					policy[j] = i;
				}
			}
		}
		
		System.out.print("policy: [ ");
		for (int i = 0; i < nStates; i++) {
			if (i == nStates - 1) System.out.print(policy[i]);
			else System.out.print(policy[i] + ", ");
		}
		System.out.println(" ]");
	}
	
	public void qlearning() {
		//init();
		
		// initialize policy
		for (int i = 0; i < nStates; i++) {
			policy[i] = 0;
		}
		
		int temp = curState;
		int curState = temp;
		
		Random rnd = new Random();
		double dice;
		int nextState = -1;
		
		// Initialize error table
		double errPrev = 0.0;
		double[][] err = new double[nStates][NUM_ACTIONS];
		for (int i = 0; i < NUM_ACTIONS; i++) {
			for (int j = 0; j < nStates; j++) {
				err[j][i] = 0.0;
			}
		}
		
		// Arbitrarily initialize Q
		for (int i = 0; i < NUM_ACTIONS; i++) {
			for (int j = 0; j < nStates; j++) {
				Q[j][i] = 0;
			}
		}
		
		// Learning
		for (int z = 0; z < step; z++) {
			int curAction = rnd.nextInt(4); //Exploration (epsilon)
			
			// Epsilon-greedy action selection from Q
			dice = rnd.nextDouble();
			if (dice > EPSILON) { // Exploitation (1 - epsilon)
				double max = Q[curState][0];
				for (int i = 0; i < NUM_ACTIONS; i++) {
					if (max < Q[curState][i]) {
						max = Q[curState][i];
						curAction = i;
					}
				}
			}
			
			// Next state candidates
			int[] stateCandidates = new int[3];
			int tempNextState = -1;
			int cnt = 0;
			for (int k = 0; k < nStates; k++) {
				double p = P[curAction][curState][k];
				if (p >= SUCCESS_FACTOR) {
					tempNextState = k; // state with highest probability
				}
				else if (p != 0) {
					stateCandidates[cnt++] = k; // other possible next states
				}
			}
			
			// Take the action, go to the next state, observe r, s'
			dice = rnd.nextDouble();
			if (dice < SUCCESS_FACTOR) {
				nextState = tempNextState; // go to desired state
			}
			else {
				int dice3 = rnd.nextInt(3);
				nextState = stateCandidates[dice3]; // go to alternative state
			}
			double curReward = R[curAction][curState];

			// Greedy action selection
			double maxQ = 0; // max_a' Q(s', a')
			for (int i = 0; i < NUM_ACTIONS; i++) {
				maxQ = max(maxQ, Q[nextState][i]);
			
			}
			
			double old = Q[curState][curAction];
			double target = curReward + DISCOUNT * maxQ;
			double e = Math.abs(target - old);
			
			err[curState][curAction] = e; // store error in the table
			
			// update Q
			double a = 0.1; // learning rate
			Q[curState][curAction] = Q[curState][curAction] + a * (curReward + DISCOUNT * maxQ - Q[curState][curAction]);
			
			// s <= s'
			curState = nextState;
			
			// error printing
			// average of all cells of the error table
			double errSum = 0;
			for (int i = 0; i < NUM_ACTIONS; i++) {
				for (int j = 0; j < nStates; j++) {
					errSum += err[j][i];
				}
			}
			double errAvg = errSum /= NUM_ACTIONS * nStates;
			
			/*
			 * uncomment the bottom line to print errAvg for each step
			 * 					|
			 * 					|
			 * 					V
			 */
			//System.out.println((z + 1) + ":   " + errAvg);
		}
		//printTable(Q);
		
		// Policy Calculation
		for (int i = 0; i < nStates; i++) {
			double max = 0;
			for (int j = 0; j < NUM_ACTIONS; j++) {
				if (max < Q[i][j]) {
					max = Q[i][j];
					policy[i] = j;
				}
			}
		}
				
		System.out.print("policy: [ ");
		for (int i = 0; i < nStates; i++) {
			if (i == nStates - 1) System.out.print(policy[i]);
			else System.out.print(policy[i] + ", ");
		}
		System.out.println(" ]");
	}
	
	
	public void sarsa() {
		//init();
		
		// initialize policy
		for (int i = 0; i < nStates; i++) {
			policy[i] = 0;
		}
		
		int temp = curState;
		int curState = temp;
		
		Random rnd = new Random();
		double dice;
		int nextState = -1;
		
		// Initialize error table
		double errPrev = 0.0;
		double[][] err = new double[nStates][NUM_ACTIONS];
		for (int i = 0; i < NUM_ACTIONS; i++) {
			for (int j = 0; j < nStates; j++) {
				err[j][i] = 0.0;
			}
		}
		
		// Arbitrarily initialize Q
		for (int i = 0; i < NUM_ACTIONS; i++) {
			for (int j = 0; j < nStates; j++) {
				Q[j][i] = 0;
			}
		}
		
		// Epsilon-greedy action selection from Q
		int curAction = rnd.nextInt(4); //Exploration (epsilon)
		dice = rnd.nextDouble();
		if (dice > EPSILON) { // Exploitation (1 - epsilon)
			double max = Q[curState][0];
			for (int i = 0; i < NUM_ACTIONS; i++) {
				if (max < Q[curState][i]) {
					max = Q[curState][i];
					curAction = i;
				}
			}
		}
		
		// Learning
		for (int z = 0; z < step; z++) {
			// Next state candidates
			int[] stateCandidates = new int[3];
			int tempNextState = -1;
			int cnt = 0;
			for (int k = 0; k < nStates; k++) {
				double p = P[curAction][curState][k];
				if (p >= SUCCESS_FACTOR) {
					tempNextState = k; // state with highest probability
				}
				else if (p != 0) {
					stateCandidates[cnt++] = k; // other possible next states
				}
			}
			
			// Take the action, go to the next state, observe r, s'
			dice = rnd.nextDouble();
			if (dice < SUCCESS_FACTOR) {
				nextState = tempNextState; // go to desired state
			}
			else {
				int dice3 = rnd.nextInt(3);
				nextState = stateCandidates[dice3]; // go to alternative state
			}
			double curReward = R[curAction][curState];

			// Epsilon-greedy action selection
			double nextQ = 0; // Q(s', a') epsilon-greedy policy
			int nextAction = rnd.nextInt(4); //Exploration (epsilon)
			dice = rnd.nextDouble();
			if (dice > EPSILON) { // Exploitation (1 - epsilon)
				double max = Q[nextState][0];
				for (int i = 0; i < NUM_ACTIONS; i++) {
					if (max < Q[nextState][i]) {
						max = Q[nextState][i];
						nextAction = i;
					}
				}
				nextQ = Q[nextState][nextAction];
			}
			else {
				nextQ = Q[nextState][nextAction];
			}
			
			double old = Q[curState][curAction];
			double target = curReward + DISCOUNT * nextQ;
			double e = Math.abs(target - old);
			
			err[curState][curAction] = e; // store error in the table
			
			// update Q
			double a = 0.1; // learning rate
			Q[curState][curAction] = Q[curState][curAction] + a * (curReward + DISCOUNT * nextQ - Q[curState][curAction]);
			
			// s <= s'
			curState = nextState;
			curAction = nextAction;
			
			// error printing
			// average of all cells of the error table
			double errSum = 0;
			for (int i = 0; i < NUM_ACTIONS; i++) {
				for (int j = 0; j < nStates; j++) {
					errSum += err[j][i];
				}
			}
			double errAvg = errSum /= NUM_ACTIONS * nStates;
			
			/*
			 * uncomment the bottom line to print errAvg for each step
			 * 					|
			 * 					|
			 * 					V
			 */
			//System.out.println((z + 1) + ":   " + errAvg);
		}
		//printTable(Q);
		
		// Policy Calculation
		for (int i = 0; i < nStates; i++) {
			double max = 0;
			for (int j = 0; j < NUM_ACTIONS; j++) {
				if (max < Q[i][j]) {
					max = Q[i][j];
					policy[i] = j;
				}
			}
		}
						
		System.out.print("policy: [ ");
		for (int i = 0; i < nStates; i++) {
			if (i == nStates - 1) System.out.print(policy[i]);
			else System.out.print(policy[i] + ", ");
		}
		System.out.println(" ]");
	}
	
	/*
	 * Helper functions
	 */
	
	public static double max(double a, double b) {
		return a >= b ? a : b;
	}
	
	public static void printTable(double[][] arr) {
		for (int i = 0; i < arr.length; i++) {
			for (int j = 0; j < arr[0].length; j++) {
				System.out.print(arr[i][j] + ",\t");
			}
			System.out.println();
		}
	}

	public static void main(String[] args) {
		RLPractice rl = new RLPractice();
		System.out.println("Value iteration:");
		rl.valueIteration();
		System.out.println("--------------------------------------------\nQ-learning:");
		rl.qlearning();
		System.out.println("--------------------------------------------\nSARSA:");
		rl.sarsa();
	}
}
