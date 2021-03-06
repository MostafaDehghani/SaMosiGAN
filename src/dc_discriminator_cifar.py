import tensorflow as tf


class Discriminator(object):
  def __init__(self, hps, scope='discriminator', depths=[64, 128, 256, 512],channels=1):
    self._hps = hps
    self._scope = scope
    self.initializer = tf.contrib.layers.xavier_initializer()
    self.depths = [channels] + depths
    self._buid_discriminator_graph()

  def _buid_discriminator_graph(self):
    pass

  def discriminate(self, x, reuse=True, training=True):
    def leaky_relu(x, leak=0.2, name=''):
      return tf.maximum(x, x * leak, name=name)

    outputs = tf.convert_to_tensor(x)

    with tf.variable_scope(self._scope, reuse=reuse) as scope:
      # convolution x 4
      with tf.variable_scope('conv1'):
        outputs = tf.layers.conv2d(outputs, self.depths[1], [4, 4], strides=(2, 2), padding='SAME')
        outputs = leaky_relu(outputs, 0.2, name='outputs')
      with tf.variable_scope('conv2'):
        outputs = tf.layers.conv2d(outputs, self.depths[2], [4, 4], strides=(2, 2), padding='SAME')
        outputs = leaky_relu(tf.layers.batch_normalization(outputs, training=training),0.2, name='outputs')
      with tf.variable_scope('conv3'):
        outputs = tf.layers.conv2d(outputs, self.depths[3], [4, 4], strides=(2, 2), padding='SAME')
        outputs = leaky_relu(tf.layers.batch_normalization(outputs, training=training), 0.2,name='outputs')
      #with tf.variable_scope('conv4'):
      #  outputs = tf.layers.conv2d(outputs, self.depths[4], [4, 4], strides=(2, 2), padding='SAME')
        outputs = leaky_relu(tf.layers.batch_normalization(outputs, training=training),0.2, name='outputs')
      with tf.variable_scope('classify'):
        batch_size = outputs.get_shape()[0].value
        tf.logging.info(batch_size)
        tf.logging.info(outputs)
        reshape = tf.reshape(outputs, [batch_size, -1])
        tf.logging.info(reshape)
        outputs = tf.layers.dense(reshape, 2, name='outputs')

    self._theta = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope="gan/" + self._scope)
    self.logit, self.prob = outputs, tf.nn.sigmoid(outputs)

    return self.prob, self.logit
