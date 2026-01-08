import javax.swing.*;
import java.awt.event.*;

public class ChillDuckApp {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Duck Button App");
        frame.setSize(400, 300);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        JLabel message = new JLabel("Press 'Yes' to summon the chill duck 😎", JLabel.CENTER);
        JButton yesButton = new JButton("Yes");
        JLabel duckLabel = new JLabel();

        int[] clicks = {0};

        yesButton.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                clicks[0]++;
                if (clicks[0] >= 3) {
                    yesButton.setEnabled(false);
                    message.setText("Here comes the chill duck!");
                    duckLabel.setIcon(new ImageIcon("C:\\Users\\91897\\IdeaProjects\\brainstorming-session-1\\src\\img.png")); // Place duck.png in your project folder
                    duckLabel.setHorizontalAlignment(JLabel.CENTER);
                } else {
                    message.setText("You pressed Yes " + clicks[0] + " time(s).");
                }
            }
        });

        frame.setLayout(new BoxLayout(frame.getContentPane(), BoxLayout.Y_AXIS));
        frame.add(message);
        frame.add(yesButton);
        frame.add(duckLabel);
        frame.setVisible(true);
    }
}
