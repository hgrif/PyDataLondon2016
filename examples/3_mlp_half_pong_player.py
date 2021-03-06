import cv2
import numpy as np
import tensorflow as tf

from common.half_pong_player import HalfPongPlayer


class MLPHalfPongPlayer(HalfPongPlayer):
    def __init__(self):
        """
        Neural network attached to pong, no way to train it yet
        """
        super(MLPHalfPongPlayer, self).__init__(run_real_time=True, force_game_fps=6)

        self._input_layer, self._output_layer = self._create_network()

        init = tf.initialize_all_variables()
        self._session = tf.Session()
        self._session.run(init)

    def _create_network(self):
        input_layer = tf.placeholder("float", [self.SCREEN_WIDTH, self.SCREEN_HEIGHT])

        feed_forward_weights_1 = tf.Variable(tf.truncated_normal([self.SCREEN_WIDTH*self.SCREEN_HEIGHT, 256], stddev=0.01))
        feed_forward_bias_1 = tf.Variable(tf.constant(0.01, shape=[256]))

        feed_forward_weights_2 = tf.Variable(tf.truncated_normal([256, self.ACTIONS_COUNT], stddev=0.01))
        feed_forward_bias_2 = tf.Variable(tf.constant(0.01, shape=[self.ACTIONS_COUNT]))

        flattened_input = tf.reshape(input_layer, shape=(1, self.SCREEN_WIDTH*self.SCREEN_HEIGHT,))

        hidden_layer = tf.nn.relu(
            tf.matmul(flattened_input, feed_forward_weights_1) + feed_forward_bias_1)

        output_layer = tf.matmul(hidden_layer, feed_forward_weights_2) + feed_forward_bias_2

        return input_layer, output_layer

    def get_keys_pressed(self, screen_array, feedback, terminal):
        # images will be black or white
        _, binary_image = cv2.threshold(cv2.cvtColor(screen_array, cv2.COLOR_BGR2GRAY), 1, 255,
                                        cv2.THRESH_BINARY)

        output = self._session.run(self._output_layer, feed_dict={self._input_layer: binary_image})
        action = np.argmax(output)

        # How do we train????

        return self.action_index_to_key(action)


if __name__ == '__main__':
    player = MLPHalfPongPlayer()
    player.start()
