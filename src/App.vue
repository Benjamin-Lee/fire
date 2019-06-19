<template>
  <div id="app" class="container">
    <h1 id="emoji" class="text-center">🔥</h1>
    <hr />
    <b-row>
      <b-col>
        <b-form>
          <b-form-group
            label-for="checkingBalance"
            label="Checking balance:"
            label-cols-lg="2"
            description="How much money is in the bank right now?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="checkingBalance"
                v-model.number="checkingBalance"
              ></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label-for="creditBalance"
            label="Credit card balance:"
            label-cols-lg="2"
            description="How much money do you owe to credit cards?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="creditBalance"
                v-model.number="creditBalance"
              ></b-form-input>
            </b-input-group>
          </b-form-group>

          <b-form-group
            label-for="remainingBudget"
            label="Remaining budget:"
            label-cols-lg="2"
            description="How much money is needed for the rest of the month?"
          >
            <b-input-group prepend="$">
              <b-form-input
                id="remainingBudget"
                v-model.number="remainingBudget"
              ></b-form-input>
            </b-input-group>
          </b-form-group>
        </b-form>
      </b-col>
    </b-row>
    <hr />
    <h2 v-if="income < 0" class="text-danger text-center">
      Oh no! There's not enough money to meet the budget. Move
      {{ (-1 * toSavings) | toUSD }} from savings to cover the shortfall. Live
      like no one else so later you can live like no one else!
    </h2>
    <h2 v-else class="text-center">
      Move <span class="text-success">{{ toSavings | toUSD }}</span> to savings,
      <span class="text-success">{{ toRetirement | toUSD }}</span> to
      retirement, and pay off the
      <span class="text-danger">{{ creditBalance | toUSD }}</span> credit
      balance. Your real income is
      <span class="text-success">{{ income | toUSD }}</span
      >.
    </h2>
  </div>
</template>

<script>
// import { mapState } from "vuex";
export default {
  name: "app",
  data() {
    return {
      checkingBalance: 0,
      creditBalance: 0,
      remainingBudget: 0,
      checkingTarget: 250,
      savingsRatio: 0.2
    };
  },
  computed: {
    // We don't just want to have the checking target in the bank; we also want
    // to be sure we can pay off our next bill
    realCheckingTarget() {
      return this.checkingTarget + this.remainingBudget;
    },
    // after paying my bills and meeting hitting the minimum I want to have in
    // the bank, what's my income?
    income() {
      return (
        this.checkingBalance - this.creditBalance - this.realCheckingTarget
      );
    },

    toSavings() {
      // first, we'll make sure that we don't have to draw from savings to pay
      // off the bills and keep our cash account funded
      if (this.income < 0) {
        return (
          -1 *
          (this.creditBalance -
            (this.checkingBalance - this.realCheckingTarget))
        );
      }

      return this.income * this.savingsRatio;
    },
    toRetirement() {
      if (this.income > 0) {
        return this.income - this.toSavings;
      }
      return 0;
    }
  },
  filters: {
    toUSD(value) {
      return value.toLocaleString(undefined, {
        currency: "USD",
        style: "currency"
      });
    }
  }
};
</script>

<style>
#app {
  margin-top: 30px;
}

#emoji {
  font-size: 500%;
}
</style>
