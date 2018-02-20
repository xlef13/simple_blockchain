import hashlib, json, sys, pickle

class block(object):

    def __init__(self, blockNumber, parentHash, contents):
        self.blockNumber = blockNumber
        self.parentHash = parentHash
        self.contents = contents
        self.hash = self.hashMe()

    def checkHash(self):
        # Raise an exception if the hash does not match the block contents
        if self.hash!=self.hashMe():
            raise Exception('Hash does not match contents of block %s'%
                            self.blockNumber)
        return

    def hashMe(self):
        if sys.version_info.major == 2:
            return unicode(hashlib.sha256(self.contents + str(self.parentHash)).hexdigest(),'utf-8')
        else:
            return hashlib.sha256(str(self.contents + str(self.parentHash)).encode('utf-8')).hexdigest()

    def __str__(self):
        description = """Number:\t%5d
            Contents:\t%s
            Parent Hash:\t%s
            Hash:\t\t%s""" % (
            self.blockNumber,
            self.contents,
            str(self.parentHash)[-10:],
            str(self.hash)[-10:]
            )
        return description

class chain(object):

    def __init__(self):
        self.blocklist = []
        try:
            self.blocklist = pickle.load(open("blockchain", "rb"))
        except IOError:
            pass
        if self.blocklist == []:
            self.blocklist.append(block(0, 0, "genesisBlock"));

    def add_block(self, contents):
        newBlock = block(len(self.blocklist), self.blocklist[-1].hash, contents)
        self.blocklist.append(newBlock);


    def json_dump_chain(self):
        for block in self.blocklist:
            s = json.dumps(block.__dict__)
            print(s)

    def print_chain(self):
        for block in self.blocklist:
            print(str(block))

    def checkBlockValidity(self, block):
        block.checkHash() # Check hash integrity; raises error if inaccurate

        if block.blockNumber < len(self.blocklist):
            if block!=self.blocklist[block.blockNumber]:
                raise Exception('Block not at appropriate position in chain %s'%block.blockNumber)
        else:
            raise Exception("chain can't contain block, number out of range %s"%block.blockNumber)
        if(block.blockNumber!=0):
            if block.parentHash != self.blocklist[block.blockNumber-1].hash:
                raise Exception('Parent hash not accurate at block %s'%block.blockNumber)

        return True

    def checkChain(self):
        for block in self.blocklist:
            self.checkBlockValidity(block)
        return True

    def search_contents_in_chain(self, contents):
        for block in self.blocklist:
            if block.contents == contents:
                return block
        return False


    def __del__(self):
        pickle.dump(self.blocklist, open("blockchain", "wb"))
        pass


import random
def create_some_blocks_and_add_to_chain(chain, amount):
    currentNumber = len(chain.blocklist)
    for i in range(amount):
        chain.add_block("Machine-ID: %5d"%random.randrange(100000,999999))

def main():
    c = chain()

    try:
        if c.checkChain():
            print("current Chain is valid")
    except Exception as e:
        print("Chain has been corrupted. %s"%str(e))
        return

    # create_some_blocks_and_add_to_chain(c, 10)
    c.print_chain()

main()
