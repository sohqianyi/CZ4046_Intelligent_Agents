/**
 * A player that combines the GrimTrigger and ForgivingT4T strategies.
 * 
 * @author Soh Qian Yi (U1922306C)
 */
class Soh_QianYi_Player extends Player {
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